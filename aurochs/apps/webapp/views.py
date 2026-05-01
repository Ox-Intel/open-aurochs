import datetime
import re
from functools import partial
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, Http404, HttpResponseNotModified
from django.utils.safestring import mark_safe
from django.shortcuts import redirect, render
from utils.helpers import reverse

from annoying.decorators import render_to, ajax_request
from django.template.loader import render_to_string
from collaboration.models import InboxItem
from frameworks.models import Framework, Criteria
from organizations.models import User
from organizations.serializers import OmniSerializer
from reports.models import Report, Scorecard, ScorecardScore
from sources.models import Source
from stacks.models import Stack


@render_to("webapp/home.html")
def app_home_handler(request):
    if request.user and not request.user.is_anonymous:
        serializer = OmniSerializer(request.user)
        js_data = serializer.serialize_to_js_lines()
        request.user.save_data_lines_to_cache(js_data)
        session_id = request.user.ox_id
    else:
        js_data = {}
        session_id = request.session.session_key
    # print(js_data)
    use_24_hour_times = "false"
    if settings.CLOCK_24_HR:
        use_24_hour_times = "true"
    return {
        "js_data": js_data,
        "session_id": session_id,
        "bugsink_dsn": getattr(settings, "BUGSINK_DSN", ""),
        "use_24_hour_times": use_24_hour_times,
        "all_users": User.objects.values(
            "ox_id", "first_name", "last_name", "username"
        ),
    }


def oxgpt(request):
    if request.user.is_anonymous and "init" not in request.session:
        request.session["init"] = "True"
    if request.user.is_anonymous:
        if "oxgpt" not in request.build_absolute_uri():
            return redirect(reverse("webapp:oxgpt"))
    return app_home_handler(request)


@login_required
def app_home(request):
    return app_home_handler(request)


def home(request):
    if request.user.is_anonymous and "init" not in request.session:
        request.session["init"] = "True"
    if request.user.is_anonymous:
        if "oxgpt" not in request.build_absolute_uri():
            return redirect(reverse("webapp:oxgpt"))
    return app_home(request)
