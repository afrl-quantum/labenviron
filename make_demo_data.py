#!/usr/bin/env python3

import random
import time

import sensorsite.outside
from labenviron.models import HostInfo, LabData

def main():
  print('About to create a sensor named "sensor1" with 100 fake data points every 2 seconds')
  input('Press enter to continue...')
  sensor1 = HostInfo(
    host='sensor1',
    location='Lab 1',
    comments='Sensor in the lab'
  )
  sensor1.save()

  T, P, H = 18, 10, 30
  for i in range(100):
    T += random.random()*1 - 0.45 # bias towards warming
    P += random.random()*1 - 0.5
    H += random.random()*3 - 1.5
    print(i+1, 'of 100: {} C, {} hPa, {} %'.format(T, P, H))
    LabData(
      host=sensor1,
      temperature=T,
      pressure=P,
      humidity=H
    ).save()
    time.sleep(2)
  

if __name__ == '__main__':
  main()
