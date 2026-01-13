import os
import sys
from os.path import join
from .common import *

try:
    from .secrets import *
except:
    pass

ALLOWED_HOSTS += [
    "*",
]
COMPRESS_ENABLED = True
SESSION_COOKIE_DOMAIN = None
SESSION_COOKIE_SECURE = False
DEV_MODE = True

AWS_STORAGE_BUCKET_NAME = "ox-aurochs-dev"
DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
DEFAULT_FILE_STORAGE = "utils.storage.AurochsFileStorage"

STATIC_PRECOMPILER_USE_CACHE = False
STATIC_PRECOMPILER_DISABLE_AUTO_COMPILE = True

if "AUROCHS_BASE_URL" in os.environ:
    MEDIA_URL = "%s/media/" % os.environ["AUROCHS_BASE_URL"]

MIDDLEWARE += ("rollbar.contrib.django.middleware.RollbarNotifierMiddleware",)
# INSTALLED_APPS += ['debug_toolbar', ]

INTERNAL_IPS = [
    # ...
    "127.0.0.1",
]

DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": "utils.middleware.show_toolbar_callback",
}
CSRF_TRUSTED_ORIGINS = [
    "https://oxe2e.ngrok.io",
    "http://oxe2e.ngrok.io",
    "https://oxe2e-airgapped.ngrok.io",
]

redis_url = urlparse(CELERY_BROKER_URL)
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": CELERY_BROKER_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
        "TIMEOUT": 15552000,  # 180 days.
    }
}


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
    },
    "loggers": {
        "django.request": {
            "handlers": ["mail_admins"],
            "level": "ERROR",
            "propagate": True,
        },
    },
    "filters": {"require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}},
}

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
LOGIN_URL = "/accounts/login/"


# CELERY_TASK_ALWAYS_EAGER = True
