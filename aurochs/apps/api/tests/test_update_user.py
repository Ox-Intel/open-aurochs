from datetime import datetime
import json
import mock
import unittest
from django.test import TestCase
from django.test import Client
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


class TestUpdateMyUser(EventTestCase):
    def test_endpoint(self):
        obj = Factory.source(user=self.user)
        data = {
            "event_type": "update_my_user",
            "first_name": Factory.rand_name(),
            "last_name": Factory.rand_name(),
            "email": Factory.rand_email(),
            "username": Factory.rand_str(include_emoji=False),
        }

        self.resp_body = self.send_event(data)

        self.assertEqual(self.resp_body["success"], True)
        self.resp_body = self.resp_body["objs"]

        # Source Data
        user_str = f"window.aurochs.data.users['{self.user.ox_id}']"
        user_data = self.get_nested_obj(f"window.aurochs.data.sources['{obj.ox_id}']")

        # User Data is included.
        user_data = self.get_nested_obj(user_str)
        self.user = User.objects.get(pk=self.user.pk)
        self.assertEqual(user_data["__type"], "user")
        # self.assertEqual(user_data["email"], self.user.email)
        # self.assertEqual(user_data["email_verified"], False)
        self.assertEqual(user_data["first_name"], self.user.first_name)
        self.assertEqual(user_data["id"], self.user.ox_id)
        self.assertEqual(user_data["last_name"], self.user.last_name)
        self.assertEqual(user_data["email"], self.user.email)
        self.assertEqual(user_data["time_zone"], None)
        self.assertEqual(user_data["username"], self.user.username)

        self.assertEqual(data["first_name"], self.user.first_name)
        self.assertEqual(data["last_name"], self.user.last_name)
        self.assertEqual(data["email"], self.user.email)
        self.assertEqual(data["username"], self.user.username)
