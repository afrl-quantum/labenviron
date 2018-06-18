"""
WSGI config for sensors project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os, sys

THIS_DIR = os.path.dirname(__file__)
PACKAGE_DIR = os.path.join(THIS_DIR, os.path.pardir)
sys.path.insert(0, PACKAGE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sensors.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
