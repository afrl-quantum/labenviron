#!/usr/bin/env python

from Adafruit_BME280 import *
import datetime, time, socket
import sensors.outside
from labenviron.models import LabData


def main():
  sensor = BME280(mode=BME280_OSAMPLE_8)
  hostname = socket.gethostname()

  # Loop to collect data for one week
  while True:
    # Read sensor data
    degrees       = sensor.read_temperature()
    hectopascals  = sensor.read_pressure() / 100.0
    humidity      = sensor.read_humidity()

    # Generate string to write to file
    ld = LabData(host=hostname,
                 temperature=degrees,
                 pressure=hectopascals,
                 humidity=humidity)
    ld.save()
    # Time interval between sensor readouts 5 minutes
    time.sleep(300)


if __name__=='__main__':
  main()
