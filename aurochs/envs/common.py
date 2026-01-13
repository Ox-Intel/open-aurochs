# -*- coding: utf-8 -*-
import logging
import mimetypes
import os
import re
import sys
from os.path import abspath, join, dirname
from sys import path

try:
    from urllib.parse import urlparse
except:
    from urlparse import urlparse

AIRGAPPED = False
DEV_MODE = False
from .configure import *

PROJECT_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
BASE_DIR = os.path.join(PROJECT_DIR, "..")
APPS_DIR = os.path.join(PROJECT_DIR, "apps")
path.insert(0, BASE_DIR)
path.insert(0, PROJECT_DIR)
path.insert(0, APPS_DIR)

MEDIA_ROOT = os.path.join(PROJECT_DIR, "media")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
IS_LIVE = False


ADMINS = ((AUROCHS_ADMIN_NAME, AUROCHS_ADMIN_EMAIL),)
MANAGERS = ADMINS

# ANYMAIL = {
#     "MAILGUN_API_KEY": MAILGUN_API_KEY,
#     "MAILGUN_SENDER_DOMAIN": MAILGUN_SENDER_DOMAIN,
# }
# EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

DEV_SETUP = False
SESSION_EXPIRES_AFTER_SECONDS = 30 * 60  # 30 minutes

EMAIL_SUBJECT_PREFIX = "%s " % AUROCHS_FRIENDLY_NAME
DEFAULT_FROM_EMAIL = "%s <%s>" % (AUROCHS_FRIENDLY_NAME, AUROCHS_FROM_EMAIL)
SERVER_EMAIL = DEFAULT_FROM_EMAIL

# For when we switch to subdomain suppport
API_DOMAIN = "api.%s" % AUROCHS_DOMAIN
WEBAPP_DOMAIN = "app.%s" % AUROCHS_DOMAIN

ALLOWED_HOSTS = [
    "*",
    AUROCHS_DOMAIN,
    API_DOMAIN,
    WEBAPP_DOMAIN,
    "ox-springbok.ngrok.io",
]
# API_BASE_URL = "https://%s" % API_DOMAIN
# WEBAPP_BASE_URL = "https://%s" % WEBAPP_DOMAIN
RESOURCES_URL = "./static/"

APPEND_SLASH = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = False

# Application definition
INSTALLED_APPS = [
    "channels",
    "django.contrib.auth",
    "django.contrib.admin",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
    "anymail",
    "binary_database_files",
    "corsheaders",
    "compressor",
    "django_celery_beat",
    "django_celery_results",
    "django_extensions",
    "simple_history",
    "static_precompiler",
    "debug_toolbar",
    "archives",
    "api",
    "collaboration",
    "frameworks",
    "files",
    "history",
    "organizations",
    "reports",
    "stacks",
    "sources",
    "utils",
    "webapp",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            # "loaders": [
            #     (
            #         "django.template.loaders.cached.Loader",
            #         [
            #             "django.template.loaders.filesystem.Loader",
            #             "django.template.loaders.app_directories.Loader",
            #             # "website.loader.Loader",
            #         ],
            #     ),
            # ],
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "utils.context_processors.is_debug",
            ],
        },
    },
]


WSGI_APPLICATION = "aurochs.wsgi.application"

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
        "TIMEOUT": 15552000,  # 180 days.
    }
}

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    # 'django_hosts.middleware.HostsRequestMiddleware',
    # 'django.middleware.cache.UpdateCacheMiddleware',
    # "inkdots.middleware.InkDotsMiddleware",
    # "django.middleware.gzip.GZipMiddleware",
    "django_brotli.middleware.BrotliMiddleware",
    "htmlmin.middleware.HtmlMinifyMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.middleware.common.BrokenLinkEmailsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware",
    # 'django.contrib.messages.middleware.MessageMiddleware',
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # 'django.middleware.cache.FetchFromCacheMiddleware',
    "htmlmin.middleware.MarkRequestMiddleware",
    # 'django_hosts.middleware.HostsResponseMiddleware',
]
IGNORABLE_404_URLS = [
    re.compile(r"\.(php|cgi)$"),
    re.compile(r"^/phpmyadmin/"),
]

ROOT_URLCONF = "aurochs.urls"
# ROOT_HOSTCONF = 'aurochs.hosts'
DEFAULT_HOST = "root"
SITE_ID = 1


CELERY_BROKER_URL = "redis://redis:6379/0"
redis_url = urlparse(CELERY_BROKER_URL)

# Channels
ASGI_APPLICATION = "aurochs.routing.application"
CHANNEL_LAYERS = {
    "default": {
        "CONFIG": {
            "hosts": [(redis_url.hostname, redis_url.port)],
        },
        # "BACKEND": "channels_redis.core.RedisChannelLayer",
        "BACKEND": "channels_redis.pubsub.RedisPubSubChannelLayer",
    },
}

AUTH_USER_MODEL = "organizations.User"
AUTHENTICATION_BACKENDS = ["utils.auth.EmailOrUsernameModelBackend"]

SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"
SESSION_SAVE_EVERY_REQUEST = True

CORS_ORIGIN_WHITELIST = (
    AUROCHS_BASE_URL,
    "http://localhost",
    "https://localhost",
)
CORS_ORIGIN_ALLOW_ALL = True


# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": POSTGRES_DB,
        "USER": POSTGRES_USER,
        "PASSWORD": POSTGRES_PASSWORD,
        "HOST": POSTGRES_HOST,
        "PORT": 5432,
    }
}
if "CIRCLECI" in os.environ:
    DATABASES["default"] = {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "circle_test",
        "USER": "ubuntu",
    }
TEST_MODE = False
DISABLE_ENCRYPTION_FOR_TESTS = False
if "test" in sys.argv:
    TEST_MODE = True
    logging.disable(logging.CRITICAL)
    CELERY_TASK_ALWAYS_EAGER = True
    CELERY_TASK_ALWAYS_EAGER = True
    CELERY_TASK_EAGER_PROPAGATES = True
    CACHES["default"]["PREFIX"] = "test"
    EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

    if (
        "DISABLE_ENCRYPTION_FOR_TESTS" in os.environ
        and os.environ["DISABLE_ENCRYPTION_FOR_TESTS"] == "True"
    ):
        DISABLE_ENCRYPTION_FOR_TESTS = True


# Static
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
)
STATIC_ROOT = join(PROJECT_DIR, "collected_static")
STATIC_URL = "/static/"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
COMPRESS_ROOT = STATIC_ROOT

COMPRESS_PRECOMPILERS = (("text/less", "lessc {infile} {outfile}"),)

COMPRESS_CSS_FILTERS = ("compressor.filters.cssmin.CSSCompressorFilter",)

# COMPRESS_JS_FILTERS = ("compressor.filters.jsmin.CalmjsFilter",)
COMPRESS_JS_FILTERS = ("compressor.filters.jsmin.JSMinFilter",)
COMPRESS_ENABLED = True
COMPRESS_OFFLINE = False
COMPRESS_CSS_HASHING_METHOD = "content"
HTML_MINIFY = True

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]
AUTH_PASSWORD_VALIDATORS = []
LOGIN_REDIRECT_URL = "/"
LOGIN_URL = "/accounts/login/"

# Background Workers
# CELERY_BROKER_URL = 'amqp://rabbitmq:rabbitmq@rabbitmq:5672'
# CELERY_BROKER_URL = 'amqp://rabbitmq:rabbitmq@rabbitmq:5672'

CELERY_BROKER_URL = "redis://redis:6379/0"
redis_url = urlparse(CELERY_BROKER_URL)


CELERY_BEAT_SCHEDULE = {}
# CELERY_ACCEPT_CONTENT = ["pickle", "json", "msgpack", "yaml"]
# CELERY_TASK_TIME_LIMIT = 15
CELERY_TASK_ROUTES = {}
CELERY_TASK_RESULT_BACKEND = "django-db"
CELERY_TASK_ALWAYS_EAGER = False
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

# Representation and calculation
from decimal import getcontext

getcontext().prec = 6

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
STATIC_URL = "/static/"

# Migrations
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Rollbar
ROLLBAR = {
    "access_token": ROLLBAR_TOKEN,
    "environment": ROLLBAR_ENV,
    "branch": "master",
    "root": BASE_DIR,
    "enabled": not DEBUG and not TEST_MODE,
}

mimetypes.add_type("application/javascript", ".js", True)


DATABASE_FILES_URL_METHOD = "URL_METHOD_2"

DATA_UPLOAD_MAX_MEMORY_SIZE = None
