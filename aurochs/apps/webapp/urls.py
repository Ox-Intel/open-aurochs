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
    re_path(r"^$", views.home, name="home"),
    re_path(r"dashboard$", views.app_home, name="dashboard"),
    re_path(r"chat$", views.app_home, name="chat"),
    re_path(r"oxgpt$", views.oxgpt, name="oxgpt"),
    re_path(r"about-ox$", views.oxgpt, name="aboutox"),
    re_path(r"teams-upgrade$", views.oxgpt, name="teamsupgrade"),
    re_path(r"library$", views.app_home, name="library"),
    re_path(r"source/.*$", views.app_home, name="source"),
    re_path(r"framework/.*$", views.app_home, name="framework"),
    re_path(r"stack/.*$", views.app_home, name="stack"),
    re_path(r"report/.*$", views.app_home, name="report"),
    re_path(r"userprofile/.*$", views.app_home, name="userprofile"),
    re_path(r"inbox$", views.app_home, name="inbox"),
    re_path(r"inbox/.*$", views.app_home, name="inbox"),
    re_path(r"teams$", views.app_home, name="teams"),
    re_path(r"guide$", views.app_home, name="guide"),
    re_path(r"users$", views.app_home, name="users"),
    re_path(r"account$", views.app_home, name="account"),
]
