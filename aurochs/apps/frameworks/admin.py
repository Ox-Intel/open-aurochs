from django.contrib import admin
from reports.models import Framework, Criteria
from utils.admin import PermissionedAdmin


@admin.register(Framework)
class FrameworkAdmin(PermissionedAdmin):
    list_display = ("admin_deleted", "name", "subtitle")
    list_display_links = ("name",)


@admin.register(Criteria)
class CriteriaAdmin(PermissionedAdmin):
    list_display = (
        "admin_deleted",
        "name",
        "framework",
        "description",
    )
    list_display_links = ("name",)
