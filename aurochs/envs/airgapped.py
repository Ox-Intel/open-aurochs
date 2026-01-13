try:
    from urllib.parse import urlparse
except:
    from urlparse import urlparse
# from memcacheify import memcacheify
# from postgresify import postgresify
from .common import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG
IS_LIVE = True
AIRGAPPED = True

SECURE_SSL_REDIRECT = False
# SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = False

# SESSION_COOKIE_DOMAIN = AUROCHS_DOMAIN
SESSION_COOKIE_NAME = "%s_id" % AUROCHS_NAMESPACE
SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"
# CORS_ORIGIN_WHITELIST = (AUROCHS_BASE_URL,)

ALLOWED_HOSTS = [
    "*",
]

DEFAULT_FILE_STORAGE = "utils.storage.AurochsFileStorage"

STATIC_PRECOMPILER_USE_CACHE = False
STATIC_PRECOMPILER_DISABLE_AUTO_COMPILE = True

EXTRA_APPS = []

# Handle Stunnel
# https://devcenter.heroku.com/articles/securing-heroku-redis
if "REDIS_URL" in os.environ:
    STUNNELED_URL = os.environ["REDIS_URL"]
    ENV_REDIS_URL = os.environ["REDIS_URL"]
else:
    base_redis_url_parts = os.environ["REDIS_URL"].split(":")
    stunnel_port = int(base_redis_url_parts[-1]) + 1
    base_redis_url_parts[-1] = str(stunnel_port)

    STUNNELED_URL = ":".join(base_redis_url_parts)
    ENV_REDIS_URL = os.environ["REDIS_URL"]

CELERY_BROKER_URL = STUNNELED_URL

FAVICON_URL = "%s/common/img/favicon.ico" % STATIC_URL

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

CHANNEL_LAYERS = {
    "default": {
        "CONFIG": {
            "hosts": [
                ENV_REDIS_URL,
            ],
        },
        "BACKEND": "channels_redis.pubsub.RedisPubSubChannelLayer",
    },
}
