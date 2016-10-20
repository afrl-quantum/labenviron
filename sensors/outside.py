
from django.conf import settings
from . import settings as sensors_settings


def prepare():
  settings.configure(DATABASES=sensors_settings.DATABASES)
