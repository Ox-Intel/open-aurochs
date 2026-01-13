from django.contrib import admin
from sources.models import Source, SourceFeedback
from utils.admin import PermissionedAdmin


@admin.register(Source)
class SourceAdmin(PermissionedAdmin):
    list_display = (
        "admin_deleted",
        "name",
        "subtitle",
    )
    list_display_links = ("name",)


# @admin.register(SourceFeedback)
# class SourceFeedbackAdmin(PermissionedAdmin):
#     list_display = (
#         "admin_deleted",
#         "source",
#         "score",
#     )
#     list_display_links = ("source",)
