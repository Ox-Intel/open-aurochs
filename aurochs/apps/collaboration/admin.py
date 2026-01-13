from django.contrib import admin
from collaboration.models import Comment
from utils.admin import PermissionedAdmin


@admin.register(Comment)
class CommentAdmin(PermissionedAdmin):
    list_display = (
        "user",
        "content_object",
    )
