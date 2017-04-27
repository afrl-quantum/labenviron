from django.db import models
from datetime import datetime
import time, numpy as np

# Create your models here.

class LabData(models.Model):
  host        = models.CharField(max_length=64)
  time        = models.DateTimeField(default=datetime.now)
  temperature = models.FloatField() # deg C
  pressure    = models.FloatField() # hPa
  humidity    = models.FloatField() # %(rel)

  class Meta:
    unique_together = (('host', 'time'),)

  def __str__(self):
    return '{}: temp: {} C, press: {} hPa, humid: {} %' \
      .format(self.time.strftime('%F %X'), self.temperature, self.pressure, self.humidity)

  def __repr__(self):
    return str(self)

  @property
  def timestamp(self):
    return time.mktime(self.time.timetuple())

  def __array__(self):
    return np.array([self.timestamp, self.temperature, self.pressure, self.humidity])

  @classmethod
  def queryset_toarray(cls, q):
    return np.array([np.array(i) for i in q])
