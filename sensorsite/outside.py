import django

if django.VERSION < (1,11):
  raise RuntimeError('use at least Django 1.11')
else:
  import os
  os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sensorsite.settings')
  django.setup()
