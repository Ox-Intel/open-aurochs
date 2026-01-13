"""
ASGI entrypoint. Configures Django and then runs the application
defined in the ASGI_APPLICATION setting.
"""

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aurochs.settings")

import django
django.setup()

from aurochs.routing import application
