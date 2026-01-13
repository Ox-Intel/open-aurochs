import json

from annoying.decorators import ajax_request
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseForbidden
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from api.events import event_handlers
from api.tasks import export_pdf
from frameworks.models import Framework
from organizations.models import User
from reports.models import Report, Scorecard
from stacks.models import Stack
from utils.helpers import is_ajax


@ajax_request
@csrf_exempt
def event(request):
    if request.method == "POST" and is_ajax(request):
        event_data = json.loads(request.body)
        if (not request.user or not request.user.is_authenticated) and (
            "event_type" not in event_data
            or not event_data["event_type"].startswith("oxgpt_")
        ):
            return HttpResponseForbidden("Access Denied.")
        event_data["_server_timestamp"] = timezone.now().timestamp() * 1000
        if event_data["event_type"] in event_handlers:
            return event_handlers[event_data["event_type"]]().handle(
                request, event_data
            )
    return {"success": False, "error_message": "Badly formatted event."}


@login_required
@csrf_exempt
@ajax_request
def export_report_pdf(request, report_id):
    # This will 500 if we don't get a POST with all the right data.
    # Potential TODO: handle errors more gracefully.

    report_id = request.POST.get("targetId", None)
    title = request.POST.get("title", None)
    org_name = request.POST.get("orgName", None)
    distribution_text = request.POST.get("distributionText", None)
    page_theme = request.POST.get("pageTheme", None)
    org_logo = request.FILES.get("orgLogo", None)

    data = {
        "report_id": report_id,
        "title": title,
        "org_name": org_name,
        "distribution_text": distribution_text,
        "page_theme": page_theme,
        "org_logo": org_logo,
        "page_domain": request.build_absolute_uri("/")[:-1],
    }

    export_pdf.delay(data, request.user.ox_id)

    return {}


@login_required
@csrf_exempt
@ajax_request
def export_stack_pdf(request, stack_id):
    # This will 500 if we don't get a POST with all the right data.
    # Potential TODO: handle errors more gracefully.

    stack_id = request.POST.get("targetId", None)
    title = request.POST.get("title", None)
    org_name = request.POST.get("orgName", None)
    distribution_text = request.POST.get("distributionText", None)
    page_theme = request.POST.get("pageTheme", None)
    org_logo = request.FILES.get("orgLogo", None)

    data = {
        "stack_id": stack_id,
        "title": title,
        "org_name": org_name,
        "distribution_text": distribution_text,
        "page_theme": page_theme,
        "org_logo": org_logo,
        "page_domain": request.build_absolute_uri("/")[:-1],
    }

    export_pdf.delay(data, request.user.ox_id)

    return {}


@login_required
@csrf_exempt
def export_scorecard_pdf(request, scorecard_id):
    # This will 500 if we don't get a POST with all the right data.
    # Potential TODO: handle errors more gracefully.

    scorecard_id = request.POST.get("scorecardId", None)
    sc = Scorecard.objects.get(ox_id=scorecard_id)

    r = Report.authorized_objects.authorize(user=request.user).findable.get(
        pk=sc.report.pk
    )

    resp = HttpResponse(
        sc.generate_pdf(
            requesting_user=request.user,
            request=request,
        ),
        content_type="application/pdf",
    )
    resp["Content-Disposition"] = f"filename={r.name}.pdf"
    return resp


@login_required
@csrf_exempt
def export_report_ppt(request, report_id, framework_id=None):
    r = Report.authorized_objects.authorize(user=request.user).findable.get(
        ox_id=report_id
    )
    framework = None
    if framework_id:
        framework = Framework.authorized_objects.authorize(
            user=request.user
        ).findable.get(ox_id=framework_id)
    bytes_str = r.report_export(file_type="ppt", framework=framework)
    bytes_str.seek(0)
    resp = HttpResponse(bytes_str.read(), content_type="application/ppt")
    resp["Content-Disposition"] = f"filename={r.name}.ppt"
    return resp


@login_required
@csrf_exempt
def export_report_png(request, report_id, framework_id=None):
    r = Report.authorized_objects.authorize(user=request.user).findable.get(
        ox_id=report_id
    )
    framework = Framework.authorized_objects.authorize(user=request.user).findable.get(
        ox_id=framework_id
    )
    bytes_str = r.report_export(file_type="png", framework=framework)
    bytes_str.seek(0)
    resp = HttpResponse(bytes_str.read(), content_type="application/png")
    resp["Content-Disposition"] = f"filename={r.name}.png"
    return resp


@login_required
@csrf_exempt
def export_framework_ppt(request, framework_id):
    fw = Framework.authorized_objects.authorize(user=request.user).findable.get(
        ox_id=framework_id
    )
    bytes_str = fw.framework_export(file_type="ppt")
    bytes_str.seek(0)
    resp = HttpResponse(bytes_str.read(), content_type="application/ppt")
    resp["Content-Disposition"] = f"filename={fw.name}.ppt"
    return resp


@login_required
@csrf_exempt
def export_framework_png(request, framework_id):
    fw = Framework.authorized_objects.authorize(user=request.user).findable.get(
        ox_id=framework_id
    )
    bytes_str = fw.framework_export(file_type="png")
    bytes_str.seek(0)
    resp = HttpResponse(bytes_str.read(), content_type="application/png")
    resp["Content-Disposition"] = f"filename={fw.name}.png"
    return resp


@login_required
@csrf_exempt
def export_framework_csv(request, framework_id):
    f = Framework.authorized_objects.authorize(user=request.user).findable.get(
        ox_id=framework_id
    )
    resp = HttpResponse(f.csv_export, content_type="application/octet-stream")
    resp["Content-Disposition"] = f"filename={f.name}.csv"
    return resp


@login_required
@csrf_exempt
def export_stack_csv(request, stack_id):
    s = Stack.authorized_objects.authorize(user=request.user).findable.get(
        ox_id=stack_id
    )
    resp = HttpResponse(s.csv_export, content_type="application/octet-stream")
    resp["Content-Disposition"] = f"filename={s.name}.csv"
    return resp


@login_required
@csrf_exempt
def export_report_csv(request, report_id):
    r = Report.authorized_objects.authorize(user=request.user).findable.get(
        ox_id=report_id
    )
    resp = HttpResponse(r.csv_export, content_type="application/octet-stream")
    resp["Content-Disposition"] = f"filename={r.name}.csv"
    return resp


@ajax_request
def login(request):
    user = "start"
    body_data = "start"
    if request.method == "POST" and is_ajax(request):
        body_data = json.loads(request.body)

        user = authenticate(
            request=request,
            username=body_data["username"],
            password=body_data["password"],
        )
        if user is not None:
            return {
                "success": True,
            }

    return {
        "success": False,
        "error_message": "Invalid username or password.",
        "user": user,
        "body": body_data,
        "method": request.method,
        "ajax": is_ajax(request),
    }
