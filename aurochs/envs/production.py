import os
import dj_database_url
import ssl

try:
    from urllib.parse import urlparse
except:
    from urlparse import urlparse

from .common import *


DEBUG = False
TEMPLATE_DEBUG = DEBUG
IS_LIVE = True

# Security settings
SECURE_SSL_REDIRECT = os.environ.get('SECURE_SSL_REDIRECT', 'True') == 'True'
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SESSION_COOKIE_DOMAIN = AUROCHS_DOMAIN
SESSION_COOKIE_NAME = "%s_id" % AUROCHS_NAMESPACE
SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"
CORS_ORIGIN_WHITELIST = (AUROCHS_BASE_URL,)

ALLOWED_HOSTS = [
    AUROCHS_DOMAIN,
    API_DOMAIN,
    WEBAPP_DOMAIN,
    'localhost',
    '127.0.0.1',
]

# Add any additional domains from environment
if 'ADDITIONAL_ALLOWED_HOSTS' in os.environ:
    ALLOWED_HOSTS.extend(os.environ['ADDITIONAL_ALLOWED_HOSTS'].split(','))

SESSION_COOKIE_SECURE = True
DEFAULT_FILE_STORAGE = "utils.storage.AurochsFileStorage"

STATIC_PRECOMPILER_USE_CACHE = False
STATIC_PRECOMPILER_DISABLE_AUTO_COMPILE = True

MIDDLEWARE += ("rollbar.contrib.django.middleware.RollbarNotifierMiddleware",)

# Email configuration (using Amazon SES)
ANYMAIL = {
    "AMAZON_SES_CLIENT_PARAMS": {
        "aws_access_key_id": AWS_ACCESS_KEY_ID,
        "aws_secret_access_key": AWS_SECRET_ACCESS_KEY,
        "region_name": AWS_S3_REGION_NAME,
    },
}
EMAIL_BACKEND = "anymail.backends.amazon_ses.EmailBackend"

# Redis configuration (simplified for standard Redis)
REDIS_URL = os.environ.get('REDIS_URL', 'redis://redis:6379/0')
CELERY_BROKER_URL = REDIS_URL

# Media files
if "AUROCHS_BASE_URL" in os.environ:
    MEDIA_URL = "%s/media/" % os.environ["AUROCHS_BASE_URL"]

FAVICON_URL = "%s/common/img/favicon.ico" % STATIC_URL

# Channels configuration for WebSockets
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [REDIS_URL],
            "capacity": 1500,
            "expiry": 2,
        },
    },
}

# Database configuration using standard DATABASE_URL
if 'DATABASE_URL' in os.environ:
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ['DATABASE_URL'],
            conn_max_age=600,
            ssl_require=os.environ.get('DATABASE_SSL_REQUIRED', 'False') == 'True'
        )
    }
else:
    # Fallback to local PostgreSQL
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ.get("POSTGRES_DB", "aurochs"),
            "USER": os.environ.get("POSTGRES_USER", "aurochs"),
            "PASSWORD": os.environ.get("POSTGRES_PASSWORD", ""),
            "HOST": os.environ.get("POSTGRES_HOST", "db"),
            "PORT": os.environ.get("POSTGRES_PORT", "5432"),
        }
    }

# Static files
STATIC_ROOT = os.path.join(BASE_DIR, 'collected_static')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
    },
}