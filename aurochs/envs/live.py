import os
import dj_database_url
import ssl

try:
    from urllib.parse import urlparse
except:
    from urlparse import urlparse
# from memcacheify import memcacheify
from postgresify import postgresify
from .common import *


DEBUG = False
TEMPLATE_DEBUG = DEBUG
IS_LIVE = True
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SESSION_COOKIE_DOMAIN = AUROCHS_DOMAIN
SESSION_COOKIE_NAME = "%s_id" % AUROCHS_NAMESPACE
SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"
CORS_ORIGIN_WHITELIST = (AUROCHS_BASE_URL,)

ALLOWED_HOSTS = [
    AUROCHS_DOMAIN,
    API_DOMAIN,
    WEBAPP_DOMAIN,
    "staging.oxintel.ai",
]

if "future." in AUROCHS_DOMAIN:
    ALLOWED_HOSTS.append("staging.%s" % ".".join(AUROCHS_DOMAIN.split(".")[1:]))

SESSION_COOKIE_SECURE = True
DEFAULT_FILE_STORAGE = "utils.storage.AurochsFileStorage"

STATIC_PRECOMPILER_USE_CACHE = False
STATIC_PRECOMPILER_DISABLE_AUTO_COMPILE = True


MIDDLEWARE += ("rollbar.contrib.django.middleware.RollbarNotifierMiddleware",)

# TODO: Switch to SES
# ANYMAIL = {
#     "MAILGUN_API_KEY": MAILGUN_API_KEY,
#     "MAILGUN_SENDER_DOMAIN": MAILGUN_SENDER_DOMAIN,
# }
# EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"
ANYMAIL = {
    "AMAZON_SES_CLIENT_PARAMS": {
        "aws_access_key_id": AWS_ACCESS_KEY_ID,
        "aws_secret_access_key": AWS_SECRET_ACCESS_KEY,
        "region_name": AWS_S3_REGION_NAME,
    },
}
EMAIL_BACKEND = "anymail.backends.amazon_ses.EmailBackend"

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
# CELERY_BROKER_URL = STUNNELED_URL


# AWS_S3_CALLING_FORMAT = 'boto.s3.connection.OrdinaryCallingFormat'
# AWS_DEFAULT_ACL = "public-read"
# AWS_S3_CUSTOM_DOMAIN = AWS_STORAGE_BUCKET_NAME
# MEDIA_URL = "https://%s.s3.amazonaws.com/" % AWS_STORAGE_BUCKET_NAME
# STATIC_URL = "https://%s.s3.amazonaws.com/" % AWS_STORAGE_BUCKET_NAME
if "AUROCHS_BASE_URL" in os.environ:
    MEDIA_URL = "%s/media/" % os.environ["AUROCHS_BASE_URL"]


FAVICON_URL = "%s/common/img/favicon.ico" % STATIC_URL

# Heroku redis SSL for websockets.
ssl_context = ssl.SSLContext()
ssl_context.check_hostname = False

heroku_redis_ssl_host = {
    "address": ENV_REDIS_URL,
    "ssl": ssl_context,
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.pubsub.RedisPubSubChannelLayer",
        "CONFIG": {
            "hosts": [
                heroku_redis_ssl_host,
            ],
        },
    },
}

redis_url = urlparse(CELERY_BROKER_URL)
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.environ.get("REDIS_URL"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"ssl_cert_reqs": None},
        },
        "TIMEOUT": 15552000,  # 180 days.
    }
}


# DATABASES = None
DATABASES = postgresify()
DATABASES["default"] = dj_database_url.config(conn_max_age=600, ssl_require=True)
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# DEFAULT_FILE_STORAGE = "utils.storage.AurochsS3Storage"
# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
# COMPRESS_STORAGE = STATICFILES_STORAGE
# COMPRESS_URL = "https://%s/" % AWS_STORAGE_BUCKET_NAME
WHITENOISE_MANIFEST_STRICT = False

# RESOURCES_URL = "https://%s/static/" % AUROCHS_DOMAIN

# COMPRESS_ENABLED = True
# # COMPRESS_OFFLINE = True
# LOGIN_URL = "login"


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "mail_admins": {
            "level": "ERROR",
            "filters": [
                "require_debug_false",
            ],
            "class": "django.utils.log.AdminEmailHandler",
        },
        "rollbar": {
            "filters": [
                "require_debug_false",
            ],
            "access_token": ROLLBAR_TOKEN,
            "environment": ROLLBAR_ENV,
            "class": "rollbar.logger.RollbarHandler",
        },
    },
    "loggers": {
        # "django.request": {
        #     "handlers": [
        #         "mail_admins",
        #     ],
        #     "level": "ERROR",
        #     "propagate": True,
        # },
        "aurochs": {
            "handlers": [
                "mail_admins",
                "rollbar",
            ],
            "level": "DEBUG",
            "propagate": True,
        },
    },
    "filters": {"require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}},
}
