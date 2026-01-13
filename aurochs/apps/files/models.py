from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.cache import cache
from django.db.models import Q
from django.contrib.auth.models import PermissionsMixin

from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.text import slugify
from simple_history.models import HistoricalRecords

from utils.encryption import create_unique_ox_id
from utils.helpers import reverse, rel
from utils.models import (
    BaseModel,
    HashidPermissionedModel,
    HasJWTMixin,
    BaseManager,
    PermissionedModel,
    HashidMixin,
    HashidBaseModel,
    DataDictMixin,
)


class UploadedFile(HashidBaseModel):
    content_type = models.ForeignKey(
        ContentType, blank=True, null=True, on_delete=models.CASCADE
    )
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey("content_type", "object_id")

    file = models.FileField(blank=True, null=True, upload_to="userfiles")

    @property
    def full_url(self):
        if settings.DEBUG:
            return f"/files{self.file.url}"
        return self.file.url
