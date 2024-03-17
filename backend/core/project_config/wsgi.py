"""
WSGI config for core project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from decouple import config as get_conf

os.environ.setdefault('DJANGO_SETTINGS_MODULE', get_conf('DJANGO_SETTINGS_MODULE'))

application = get_wsgi_application()
