import json
import urllib.request
from urllib.parse import urlparse

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


@csrf_exempt
@require_POST
def bugsink_tunnel(request):
    try:
        envelope = request.body.decode("utf-8")
        header = json.loads(envelope.split("\n")[0])
        dsn = urlparse(header.get("dsn", ""))
        project_id = dsn.path.strip("/")
        bugsink_url = f"https://{dsn.hostname}/api/{project_id}/envelope/"
    except (json.JSONDecodeError, KeyError, AttributeError):
        return HttpResponse(status=400)

    req = urllib.request.Request(
        bugsink_url,
        data=request.body,
        headers={"Content-Type": "text/plain;charset=UTF-8"},
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            return HttpResponse(status=resp.status)
    except Exception:
        return HttpResponse(status=502)
