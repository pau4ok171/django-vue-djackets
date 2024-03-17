"""
ASGI config for core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from decouple import config as get_conf

os.environ.setdefault('DJANGO_SETTINGS_MODULE', get_conf('DJANGO_SETTINGS_MODULE'))

application = get_asgi_application()
