#!/usr/bin/env python3

from Adafruit_BME280 import *
import datetime, time, socket, argparse
import sensorsite.outside
from labenviron.models import HostInfo, LabData


def main(interval):
  sensor = BME280(t_mode=BME280_OSAMPLE_8,
                  p_mode=BME280_OSAMPLE_8,
                  h_mode=BME280_OSAMPLE_8)

  # first thing is to get  our host object
  host = HostInfo.objects.get_or_create(host=socket.gethostname())[0]

  # Loop to collect data for one week
  while True:
    # Read sensor data
    degrees       = sensor.read_temperature()
    hectopascals  = sensor.read_pressure() / 100.0
    humidity      = sensor.read_humidity()

    # Generate string to write to file
    ld = LabData(host=host,
                 temperature=degrees,
                 pressure=hectopascals,
                 humidity=humidity)
    ld.save()
    # Time interval between sensor readouts 5 minutes
    time.sleep(interval)


if __name__=='__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--interval', default=300, type=int,
    help='Specify the time interval in seconds [Default 300]')
  args = parser.parse_args()
  main(args.interval)
