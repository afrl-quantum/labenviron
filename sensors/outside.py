import django

if django.VERSION < (1,7):
  from django.conf import settings
  from . import settings as sensors_settings

  settings.configure(
    DATABASES=sensors_settings.DATABASES,
    TIME_ZONE='America/Denver',
  )
else:
  import os
  os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sensors.settings')
  django.setup()
