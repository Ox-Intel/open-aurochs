import json
import os
import re
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt
from django.http import (
    HttpResponse,
    Http404,
    HttpResponseNotModified,
    HttpResponseForbidden,
)
from django.utils.safestring import mark_safe

from annoying.decorators import render_to, ajax_request
from django.template.loader import render_to_string
from collaboration.models import InboxItem
from frameworks.models import Framework, Criteria
from organizations.models import User
from organizations.serializers import OmniSerializer
from reports.models import Report, Scorecard, ScorecardScore
from sources.models import Source
from stacks.models import Stack
from files.models import UploadedFile


@ajax_request
@csrf_exempt
def upload(request):
    object_pk = request.POST["ox_id"]
    object_type = request.POST["object_type"]

    obj = None
    if object_type == "stack":
        obj = Stack.authorized_objects.authorize(user=request.user).findable.get(
            ox_id=object_pk
        )
    elif object_type == "source":
        obj = Source.authorized_objects.authorize(user=request.user).findable.get(
            ox_id=object_pk
        )
    elif object_type == "report":
        obj = Report.authorized_objects.authorize(user=request.user).findable.get(
            ox_id=object_pk
        )
    elif object_type == "framework":
        obj = Framework.authorized_objects.authorize(user=request.user).findable.get(
            ox_id=object_pk
        )

    if not obj:
        return HttpResponseForbidden

    f = UploadedFile.objects.create(file=request.FILES["file"], content_object=obj)
    print(f.full_url)
    return {"success": True, "url": f.full_url}
