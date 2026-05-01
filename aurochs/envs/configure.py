from os import environ

# Map namespaced or arbritrary environment keys to names in settings.
KEY_MAPPING = {"DJANGO_SECRET_KEY": "SECRET_KEY"}


def set_required_key(key, fallback=None):
    if (
        (key not in globals() or globals()[key] is None)
        and key in environ
        or fallback
        or fallback is False
    ):
        if key in environ:
            key_val = environ[key]
            if key_val == "true" or key_val == "True":
                key_val = True
            if key_val == "false" or key_val == "False":
                key_val = False
            if key in KEY_MAPPING:
                globals()[KEY_MAPPING[key]] = key_val
            else:
                globals()[key] = key_val
            return
        else:
            if fallback or fallback is False:
                globals()[key] = fallback
                return

    raise KeyError(
        "Missing %s variable.  Please set in .env file, and try again." % key
    )


# Django configuration
# Internal private key, used for security.  Keep this safe!
set_required_key("DJANGO_SECRET_KEY")

# Aurochs configuration

# Friendly name, used for internal communication
set_required_key("AUROCHS_FRIENDLY_NAME")

# Unique name for the shop, used to configure internal services
set_required_key("AUROCHS_NAMESPACE")

# Shop encryption key, used to encrypt customer data.  Keep this safe, and keep a backup!
set_required_key("AUROCHS_ENCRYPTION_KEY")
set_required_key("AUROCHS_ENCRYPTION_SALT")

# The base URL for the shop.
set_required_key("AUROCHS_DOMAIN", environ.get("HEROKU_APP_NAME", ""))
globals()["AUROCHS_BASE_URL"] = "https://%s" % globals()["AUROCHS_DOMAIN"]

# Shop admin's name
set_required_key("AUROCHS_ADMIN_NAME")

# Shop admin's email address
set_required_key("AUROCHS_ADMIN_EMAIL")

# The default email address that outgoing email should be sent from
set_required_key("AUROCHS_FROM_EMAIL")


# AWS
set_required_key("AWS_STORAGE_BUCKET_NAME", "not set")
set_required_key("AWS_S3_HOST", "not set")
set_required_key("AWS_ACCESS_KEY_ID", "not set")
set_required_key("AWS_SECRET_ACCESS_KEY", "not set")
set_required_key("AWS_S3_REGION_NAME", "us-east-2")
AWS_S3_SIGNATURE_VERSION = "s3v4"
AWS_DEFAULT_ACL = "private"
AWS_PRESIGNED_EXPIRY = 3600


# Database config
set_required_key("POSTGRES_DB", "not set")
set_required_key("POSTGRES_USER", "not set")
set_required_key("POSTGRES_PASSWORD", "not set")
set_required_key("POSTGRES_HOST", "db")
set_required_key("CLOCK_24_HR", False)
set_required_key("AIRGAPPED", True)
set_required_key("TEMP_NO_PUBLIC", False)

set_required_key("HASHID_SALT", fallback="iALkYUc")
set_required_key("METAPHOR_KEY", fallback="none")

set_required_key("BUGSINK_DSN", fallback="not set")
