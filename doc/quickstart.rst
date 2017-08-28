.. _quickstart:

Quick Start
============
The Adafruit BME280 development board uses the BME280 chip from Bosch in order
to very cheaply provide measurements for temperature, pressure, and humidity.
Each of these measurements typically has impact on the stability of a laboratory
environment where standard optics mounts, lenses, mirrors, etc are used.
This webapp uses Python Django to both record data into any arbitrary database
as well as present data to the user with a webapp.

*********************
Pre-requisites
*********************
In order to use this code, you must install at least the following packages from
Adafruit
  - Adafruit_BME280.py
  - Adafruit_GPIO

*********************
sensors/settings.py
*********************
In most cases, configuring this webapp for use consists of changing a few
small entries in sensors/settings.py:
  - The most critical of these two will be the database configuration.  Thanks
    to Django, this code is somewhat agnostic to the particular version and
    flavor of the database that you wish to use.  Please just follow standard
    Django database settings to connect to your own favorite database.
  - You may also choose to edit:
      - DEBUG (if you choose to deploy this in any real environment)
      - TIME_ZONE (default: America/Denver)
      - LANGUAGE_CODE (default: en-us)
      - STATIC_ROOT (if you deploy this in a real web environment)

*********************
Recording Data
*********************
Recording data is simple.  Just execute the record_sensors.py script on the
machine with the Adafruit BME280 development board connected.  This script can
also be given an '--interval' commandline parameter to set the interval between
measurements (defaults to 300s).

.. code-block:: bash

  python ./record_sensors.py [--interval INTERVAL]


*********************
Presenting the Data
*********************
If desired, one can also use the measurement node to also present the data in a
small django test webserver.  This is simply done by

.. code-block:: bash

  python ./manage.py runserver 0.0.0.0:8000


One can also use deploy the presentation to a real webserver, such as Apache.
It is beyond the scope of this guide to describe the proper method of deploying
a Django webapp in an environment such as Apache.  Please refer to Django
documentation and the documentation of your webserver.
