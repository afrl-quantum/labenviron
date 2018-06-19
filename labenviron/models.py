from django.db import models
from datetime import datetime
import time, numpy as np

from matplotlib.dates import date2num

# Create your models here.

class HostInfo(models.Model):
  host        = models.CharField(max_length=64, primary_key=True)
  location    = models.CharField(max_length=64, null=True, blank=True)
  comments    = models.TextField(null=True, blank=True)

  def __str__(self):
    return self.host

  def __unicode__(self):
    return unicode(str(self))

  def __repr__(self):
    return '<{}>'.format(self)

class LabData(models.Model):
  host        = models.ForeignKey(HostInfo, max_length=64)
  time        = models.DateTimeField(default=datetime.now)
  temperature = models.FloatField() # deg C
  pressure    = models.FloatField() # hPa
  humidity    = models.FloatField() # %(rel)

  class Meta:
    unique_together = (('host', 'time'),)

  def __str__(self):
    return 'host: {}, time: {}, temp: {} C, press: {} hPa, humid: {} %' \
      .format(self.host, self.time.strftime('%F %X'), self.temperature, self.pressure, self.humidity)

  def __repr__(self):
    return str(self)

  def __unicode__(self):
    return unicode(str(self))

  @property
  def timestamp(self):
    return time.mktime(self.time.timetuple())

  @property
  def ordinal(self):
    return date2num(self.time)


  array_order = ['time[gregorian date]', 'Temperature', 'Pressure', 'Humidity']
  def __array__(self):
    return np.array([self.ordinal, self.temperature, self.pressure, self.humidity])

  @classmethod
  def queryset_toarray(cls, q):
    return np.array([np.array(i) for i in q])
