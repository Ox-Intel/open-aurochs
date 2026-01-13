# -*- coding: utf-8 -*-
from django.contrib import admin
from django.conf.urls import include
from django.urls import path, re_path

# from django.contrib import accounts
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.views.static import serve
from utils.auth import (
    AurochsPasswordResetView,
    AurochsLoginView,
    AurochsLoginForm,
    AurochsPasswordResetConfirmView,
)
from binary_database_files import views as db_views
import debug_toolbar

admin.site.site_header = "Ox Admin"
admin.site.site_title = "Ox Admin Portal"
admin.site.index_title = "Welcome to Ox Admin Portal"

urlpatterns = [
    re_path(r"^", include(("webapp.urls", "webapp"), namespace="webapp")),
    # re_path(r"^public/", include(("public.urls", "public"), namespace="public")),
    re_path(r"^", include(("files.urls", "files"), namespace="files")),
    re_path(r"^files/(?P<name>.+)$", db_views.serve_mixed, name="database_file"),
    re_path(r"^", include(("api.urls", "api"), namespace="api")),
    path("administration/", admin.site.urls),
    re_path(
        r"^accounts/password_reset/$",
        AurochsPasswordResetView.as_view(
            template_name="accounts/password_reset_form.html",
            email_template_name="accounts/password_reset_email.html",
        ),
        name="password_reset",
    ),
    re_path(
        r"^accounts/password_reset/done/$",
        auth_views.PasswordResetDoneView.as_view(
            template_name="accounts/password_reset_done.html",
        ),
        name="password_reset_done",
    ),
    path(
        "accounts/password-reset-confirm/<uidb64>/<token>/",
        AurochsPasswordResetConfirmView.as_view(
            template_name="accounts/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    re_path(
        "^accounts/password-reset-complete/$",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    re_path(
        r"^accounts/login/$",
        AurochsLoginView.as_view(
            authentication_form=AurochsLoginForm, template_name="accounts/login.html"
        ),
        name="login",
    ),
    re_path(
        r"^accounts/logout/$",
        auth_views.LogoutView.as_view(
            template_name="accounts/logout.html",
            next_page="/",
        ),
        name="logout",
    ),
]
# if not settings.AIRGAPPED:
#     urlpatterns += [
#         re_path(r"^", include(("public.urls", "public"), namespace="public")),
#     ]


if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
        re_path(
            r"^media/(?P<path>.*)$",
            serve,
            {
                "document_root": settings.MEDIA_ROOT,
            },
        ),
    ]
    urlpatterns += staticfiles_urlpatterns()
