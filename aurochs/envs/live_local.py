from .live import *

# DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
DEFAULT_FILE_STORAGE = "utils.storage.AurochsFileStorage"
COMPRESS_STORAGE = DEFAULT_FILE_STORAGE
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
