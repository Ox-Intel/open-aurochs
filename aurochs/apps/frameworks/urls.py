# -*- coding: utf-8 -*-
from django.conf.urls import include
from django.contrib import admin
from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.views.static import serve

from . import views

urlpatterns = [
    re_path(r"^sitemap.xml$", views.sitemap, name="sitemap"),
    re_path(r"^favicon.ico$", views.favicon, name="favicon"),
    re_path(r"^privacy$", views.privacy, name="privacy"),
    re_path(r"^static/(?P<resource_slug>.*)$", views.resource, name="resource"),
    re_path(r"^(?P<page_slug>.*)$", views.page_or_post, name="page_or_post"),
    re_path(r"^$", views.page_or_post, name="root_page_or_post"),
]

if settings.DEBUG:
    urlpatterns += [
        re_path(
            r"^media/(?P<path>.*)$",
            serve,
            {
                "document_root": settings.MEDIA_ROOT,
            },
        ),
    ]
    urlpatterns += staticfiles_urlpatterns()
