import os
import sys
from os.path import join
from .dev import *


try:
    from .secrets import *
except:
    pass

redis_url = urlparse(CELERY_BROKER_URL)
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": CELERY_BROKER_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
        "TIMEOUT": 15552000,  # 180 days.
        "KEY_PREFIX": "UNITTESTS",
    }
}

# MIDDLEWARE += ("rollbar.contrib.django.middleware.RollbarNotifierMiddleware",)
