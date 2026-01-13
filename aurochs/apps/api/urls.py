from django.urls import path
from django.views.generic.base import RedirectView

from api import views

urlpatterns = [
    # ...
    path("event/", views.event, name="event"),
    path(
        "export/framework/ppt/<slug:framework_id>/",
        views.export_framework_ppt,
        name="export_framework_ppt",
    ),
    path(
        "export/framework/png/<slug:framework_id>/",
        views.export_framework_png,
        name="export_framework_png",
    ),
    path(
        "export/framework/csv/<slug:framework_id>/",
        views.export_framework_csv,
        name="export_framework_csv",
    ),
    path(
        "export/stack/csv/<slug:stack_id>/",
        views.export_stack_csv,
        name="export_stack_csv",
    ),
    path(
        "export/report/csv/<slug:report_id>/",
        views.export_report_csv,
        name="export_report_csv",
    ),
    path(
        "export/report/ppt/<slug:report_id>/",
        views.export_report_ppt,
        name="export_report_ppt",
    ),
    path(
        "export/report/pdf/<slug:report_id>/",
        views.export_report_pdf,
        name="export_report_pdf",
    ),
    path(
        "export/scorecard/pdf/<slug:scorecard_id>/",
        views.export_scorecard_pdf,
        name="export_scorecard_pdf",
    ),
    path(
        "export/stack/pdf/<slug:stack_id>/",
        views.export_stack_pdf,
        name="export_stack_pdf",
    ),
    path(
        "export/report/ppt/<slug:report_id>/<slug:framework_id>",
        views.export_report_ppt,
        name="export_report_ppt",
    ),
    path(
        "export/report/png/<slug:report_id>/<slug:framework_id>",
        views.export_report_png,
        name="export_report_png",
    ),
    # path("login/", views.login, name="login"),
    path("login/", RedirectView.as_view(url="/accounts/login/")),
]
