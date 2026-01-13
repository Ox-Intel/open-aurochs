# -*- coding: utf-8 -*-
from django.conf import settings
from django_hosts import patterns, host

host_patterns = patterns(
    "",
    host(r"", "aurochs.host_urls.root", name="root"),
)
