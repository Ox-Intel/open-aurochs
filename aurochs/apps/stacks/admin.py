from django.contrib import admin
from stacks.models import Stack
from utils.admin import PermissionedAdmin


@admin.register(Stack)
class StackAdmin(PermissionedAdmin):
    list_display = (
        "admin_deleted",
        "name",
        "subtitle",
    )
    list_display_links = ("name",)
    fields = ("name", "subtitle", "notes")
