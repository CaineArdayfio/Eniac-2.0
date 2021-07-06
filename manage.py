#!/usr/bin/env python
"""
Copyright (c) 2019 - present AppSeed.us
dj_database_url==0.5.0
Unipath==1.1
pandas==0.24.2
twilio==6.53.0
python-decouple==3.4
python_dateutil==2.8.1
asgiref
autopep8
Django>=3.0,<=3.1
pycodestyle
pytz
sqlparse
Unipath
gunicorn
whitenoise
mysqlclient
"""

import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
