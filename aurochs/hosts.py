# -*- coding: utf-8 -*-
from django.conf import settings
from django_hosts import patterns, host

if hasattr(settings, "IS_LIVE") and settings.IS_LIVE:
    host_patterns = patterns(
        "",
        host(r"", "aurochs.host_urls.webapp", name="root"),
        host(r"api", "aurochs.host_urls.api", name="api"),
        host(r"webapp", "aurochs.host_urls.webapp", name="webapp"),
    )
else:
    host_patterns = patterns(
        "",
        host(r"", "aurochs.host_urls.webapp", name="root"),
        host(r"api", "aurochs.host_urls.api", name="api"),
        host(r"webapp", "aurochs.host_urls.webapp", name="webapp"),
    )
