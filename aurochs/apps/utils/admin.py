from django.contrib.auth.models import Group
from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from django_celery_beat.models import (
    IntervalSchedule,
    CrontabSchedule,
    SolarSchedule,
    ClockedSchedule,
    PeriodicTask,
)
from django_celery_results.models import GroupResult, TaskResult

admin.site.unregister(SolarSchedule)
admin.site.unregister(ClockedSchedule)
admin.site.unregister(PeriodicTask)
admin.site.unregister(IntervalSchedule)
admin.site.unregister(CrontabSchedule)
admin.site.unregister(GroupResult)
admin.site.unregister(TaskResult)
admin.site.unregister(Group)


class SoftDeleteAdmin(SimpleHistoryAdmin):
    def admin_deleted(self, obj):
        return not obj.deleted

    admin_deleted.short_description = "Active"
    admin_deleted.boolean = True


class PermissionedAdmin(SoftDeleteAdmin):
    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_module_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def get_queryset(self, request):
        return self.model.objects_with_deleted.get_queryset()
