from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from files.models import UploadedFile
from utils.admin import PermissionedAdmin, SoftDeleteAdmin


@admin.register(UploadedFile)
class UploadedFileAdmin(SoftDeleteAdmin):
    list_display = ("content_type", "object_id", "file")
    list_filter = []
    fieldsets = None
    fields = ["content_type", "object_id", "file"]
