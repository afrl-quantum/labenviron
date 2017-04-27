from django.db import models
from datetime import datetime

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
