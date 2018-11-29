"""
WSGI config for finalproject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os
import sys
import django

sys.path.insert(0, '/opt/python/current/app')

os.environ['DJANGO_SETTINGS_MODULE'] = 'finalproject.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
