from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from organizations.models import (
    User,
    Organization,
    OrganizationRole,
    Team,
    TeamMember,
    Tag,
    GenericPermission,
)
from utils.admin import PermissionedAdmin, SoftDeleteAdmin


@admin.register(User)
class UserAdmin(BaseUserAdmin, SoftDeleteAdmin):
    list_display = (
        "username",
        "email",
        "created_at",
        # "password",
        # "is_ox_staff",
    )
    list_filter = [
        "created_at",
        "public_signup",
    ]
    fieldsets = None
    fields = [
        "first_name",
        "last_name",
        "email",
        "username",
        "time_zone",
        "password",
        "is_superuser",
        "is_ox_staff",
        "public_signup",
    ]
    exclude = [
        "groups",
        "user_permissions",
        "email_verified",
        "legacy_password",
        "legacy_password_migrated",
        "legacy_user",
        "legacy_pk",
        "is_ox_staff",
        "is_active",
        "date_joined",
        "is_staff",
    ]


@admin.register(OrganizationRole)
class OrganizationRoleAdmin(SoftDeleteAdmin):
    list_display = (
        "admin_deleted",
        "user",
        "organization",
        "can_view",
        "can_manage",
    )
    list_display_links = ("user",)
    exclude = [
        "created_by",
        "created_at",
        "modified_at",
        "modified_by",
        "deleted",
        "deleted_at",
        "legacy_pk",
    ]


class OrganizationRoleInline(admin.TabularInline):
    model = OrganizationRole
    fields = (
        "user",
        "can_view",
        "can_manage",
    )


@admin.register(Organization)
class OrganizationAdmin(SoftDeleteAdmin):
    list_display = (
        "admin_deleted",
        "name",
    )
    search_fields = ("name",)
    list_display_links = ("name",)
    inlines = [
        OrganizationRoleInline,
    ]
    exclude = [
        "created_by",
        "created_at",
        "modified_at",
        "modified_by",
        "deleted",
        "deleted_at",
        "legacy_pk",
    ]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            # Do something with `instance`
            instance.save()
        formset.save_m2m()


@admin.register(TeamMember)
class TeamMemberAdmin(SoftDeleteAdmin):
    list_display = (
        "admin_deleted",
        "user",
        "team",
        "can_view",
        "can_manage",
    )
    list_display_links = ("user",)
    exclude = [
        "created_by",
        "created_at",
        "modified_at",
        "modified_by",
        "deleted",
        "deleted_at",
        "legacy_pk",
    ]


class TeamMemberInline(admin.TabularInline):
    model = TeamMember
    fields = (
        "user",
        "can_view",
        "can_manage",
    )


@admin.register(Team)
class TeamAdmin(SoftDeleteAdmin):
    list_display = (
        "admin_deleted",
        "name",
        "organization",
    )
    list_display_links = ("name",)
    inlines = [
        TeamMemberInline,
    ]
    exclude = [
        "created_by",
        "created_at",
        "modified_at",
        "modified_by",
        "deleted",
        "deleted_at",
        "legacy_pk",
    ]

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            # Do something with `instance`
            instance.save()
        formset.save_m2m()


@admin.register(Tag)
class TagAdmin(SoftDeleteAdmin):
    list_display = (
        "name",
        "organization",
        "user",
    )
    list_filter = []
    fieldsets = None
    fields = [
        "name",
        "slug",
        "organization",
        "user",
    ]


@admin.register(GenericPermission)
class GenericPermissionAdmin(SoftDeleteAdmin):
    list_display = (
        "content_object",
        "team",
        "organization",
        "user",
    )
    list_filter = []
    fieldsets = None
    fields = [
        "content_type",
        "object_id",
        "team",
        "organization",
        "user",
    ]
