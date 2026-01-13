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


class TestGetMyUser(EventTestCase):
    def test_endpoint(self):
        obj = Factory.source(user=self.user)
        data = {
            "event_type": "get_my_user",
        }

        self.resp_body = self.send_event(data)

        self.assertEqual(self.resp_body["success"], True)
        self.resp_body = self.resp_body["objs"]

        # Source Data
        user_str = f"window.aurochs.data.users['{self.user.ox_id}']"
        user_data = self.get_nested_obj(f"window.aurochs.data.sources['{obj.ox_id}']")

        # User Data is included.
        user_data = self.get_nested_obj(user_str)
        self.assertEqual(user_data["__type"], "user")
        # self.assertEqual(user_data["email"], self.user.email)
        # self.assertEqual(user_data["email_verified"], False)
        self.assertEqual(user_data["first_name"], self.user.first_name)
        self.assertEqual(user_data["id"], self.user.ox_id)
        self.assertEqual(user_data["last_name"], self.user.last_name)
        self.assertEqual(user_data["organizations"], [])
        self.assertEqual(user_data["teams"], [])
        self.assertEqual(user_data["time_zone"], None)
        self.assertEqual(user_data["username"], self.user.username)
        self.assertEqual(
            user_data["inbox"],
            {
                "active": [],
                "done": [],
                "unread_count": 0,
            },
        )
