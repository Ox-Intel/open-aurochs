from django.conf.urls import include, url
from django.urls import path, re_path
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.views.static import serve
from django.contrib.auth import views as auth_views
from utils.auth import AurochsPasswordResetView, AurochsLoginView

urlpatterns = [
    url(r"^", include(("webapp.urls", "webapp"), namespace="webapp")),
    # url(r"^public/", include(("public.urls", "public"), namespace="public")),
    url(r"^", include(("files.urls", "files"), namespace="files")),
    url(r"^", include(("api.urls", "api"), namespace="api")),
    url(r"administration/", admin.site.urls),
    url(
        r"^accounts/password_reset/$",
        AurochsPasswordResetView.as_view(),
        name="accounts_password_reset",
    ),
    url(
        r"^accounts/password_reset/$",
        AurochsPasswordResetView.as_view(),
        name="password_reset",
    ),
    url(
        r"^accounts/password_reset/done/$",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    url(
        r"^accounts/login/$",
        AurochsLoginView.as_view(),
        {
            "template_name": "login.html",
        },
        name="login",
    ),
    url(
        r"^accounts/logout/$",
        auth_views.LogoutView.as_view(),
        {"next_page": "/"},
        name="logout",
    ),
    url(
        r"^accounts/password-reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    url(
        r"^accounts/password-reset/done/$",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]


if settings.DEBUG:
    urlpatterns += [
        url(
            r"^media/(?P<path>.*)$",
            serve,
            {
                "document_root": settings.MEDIA_ROOT,
            },
        ),
    ]
    urlpatterns += staticfiles_urlpatterns()
