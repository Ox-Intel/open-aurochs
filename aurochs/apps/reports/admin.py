from django.contrib import admin
from reports.models import Report, Scorecard, ScorecardScore
from utils.admin import PermissionedAdmin


@admin.register(Report)
class ReportAdmin(PermissionedAdmin):
    list_display = (
        "admin_deleted",
        "name",
        "subtitle",
    )
    list_display_links = ("name",)


@admin.register(Scorecard)
class ScorecardAdmin(PermissionedAdmin):
    list_display = (
        "admin_deleted",
        "report",
        "framework",
        "scorer",
    )
    list_display_links = ("report",)


@admin.register(ScorecardScore)
class ScorecardScoreAdmin(PermissionedAdmin):
    list_display = (
        "admin_deleted",
        "scorecard",
        "criteria",
        "score",
        "comment",
        "gpt_scored_last",
        "gpt_score",
    )
    list_display_links = ("scorecard",)
