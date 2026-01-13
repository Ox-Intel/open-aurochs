from datetime import datetime
import json
import mock
import unittest
from django.test import TestCase, Client, override_settings
from django.conf import settings
from django_webtest import WebTest
from utils.factory import Factory
from api.tests.base import EventTestCase

from frameworks.models import Criteria, Framework
from organizations.models import (
    Organization,
    Team,
    TeamMember,
    User,
    OrganizationRole,
)
from reports.models import Report, Scorecard, ScorecardScore
from sources.models import Source, SourceFeedback


@override_settings(
    STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage",
    AIRGAPPED=False,
    TEMP_NO_PUBLIC=False,
)
class TestLoginPublic(WebTest):
    csrf_checks = False

    def test_page(self):
        self.user, self.password = Factory.user()

        resp = self.app.post(
            "/event/",
            json.dumps({"event_type": "get_frameworks"}),
            content_type="application/json",
            xhr=True,
            status=403,
        )
        self.assertEqual(resp.status_code, 403)

        # Go to the login page
        # resp = self.app.get("/")
        resp = self.app.get("/dashboard").follow()

        form = self.app.get(resp.context["request"].environ["PATH_INFO"]).form
        form["username"] = self.user.username
        form["password"] = self.password
        resp = form.submit().follow()
        try:
            while True:
                resp = resp.follow()
        except:
            pass
        self.assertEqual(resp.status_code, 200)

        resp = self.app.post(
            "/event/",
            json.dumps({"event_type": "get_frameworks"}),
            content_type="application/json",
            xhr=True,
        )
        self.assertEqual(resp.status_code, 200)


# @override_settings(
#     STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage",
#     AIRGAPPED=True,
# )
# class TestLoginAirgapped(WebTest):
#     csrf_checks = False

#     def test_page(self):
#         self.user, self.password = Factory.user()
#         resp = self.app.post(
#             "/event/",
#             json.dumps({"event_type": "get_frameworks"}),
#             content_type="application/json",
#             xhr=True,
#             status=403,
#         )
#         self.assertEqual(resp.status_code, 403)

#         # Go to the login page
#         resp = self.app.get("/").follow()

#         form = self.app.get(resp.context["request"].environ["PATH_INFO"]).form
#         form["username"] = self.user.username
#         form["password"] = self.password
#         resp = form.submit().follow()
#         try:
#             while True:
#                 resp = resp.follow()
#         except:
#             pass
#         self.assertEqual(resp.status_code, 200)

#         resp = self.app.post(
#             "/event/",
#             json.dumps({"event_type": "get_frameworks"}),
#             content_type="application/json",
#             xhr=True,
#         )
#         self.assertEqual(resp.status_code, 200)
