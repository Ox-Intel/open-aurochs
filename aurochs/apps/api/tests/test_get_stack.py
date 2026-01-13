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
from stacks.models import Stack


class TestGetStack(EventTestCase):
    def test_endpoint(self):
        obj = Factory.stack(user=self.user)
        data = {
            "event_type": "get_stack",
            "id": obj.ox_id,
        }

        sent_time = self.now()
        self.resp_body = self.send_event(data)

        self.assertEqual(self.resp_body["success"], True)
        self.resp_body = self.resp_body["objs"]

        obj_data = self.get_nested_obj(f"window.aurochs.data.stacks['{obj.ox_id}']")

        # Stack Data
        user_str = f"window.aurochs.data.users['{self.user.ox_id}']"
        # "window.aurochs.data.stacks['1']": '{"__type": "stack",
        self.assertEqual(obj_data["__type"], "stack")

        self.assertEqual(
            obj_data["permissions"],
            {
                f"U-{self.user.ox_id}": "1111",
            },
        )
        # "created_at": "2022-04-12T19:18:30.437Z",
        self.assertBasicallyEqualTimes(
            datetime.fromtimestamp(int(obj_data["created_at_ms"]) / 1000), sent_time
        )
        # "created_at_ms": 1649791110437.731,
        # "created_by": user,
        self.assertEqual(obj_data["created_by"], user_str)
        # "deleted": false,

        # "deleted_at": null,

        # "subtitle": "Early.",
        self.assertEqual(obj_data["subtitle"], obj.subtitle)
        # "id": 1,
        self.assertEqual(obj_data["id"], obj.ox_id)
        # "modified_at": "2022-04-12T19:18:30.443Z",
        # "modified_at_ms": 1649791110443.849,
        # "modified_by": null,

        # "name": "R\\u2764\\ud83c\\udf81\\ud83d\\udc8cF\\u2642\\ud83c\\udfa7\\ud83c\\udf31Dl",
        self.assertEqual(obj_data["name"], obj.name)

        # User Data is included.
        user_data = self.get_nested_obj(user_str)
        # '__type': 'user',
        self.assertEqual(user_data["__type"], "user")
        # 'email': 'claire33@example.org',
        # self.assertEqual(user_data["email"], self.user.email)
        # 'email_verified': False,
        # self.assertEqual(user_data["email_verified"], False)
        # 'first_name': 'Micah',
        self.assertEqual(user_data["first_name"], self.user.first_name)
        # 'id': 4,
        self.assertEqual(user_data["id"], self.user.ox_id)
        # 'last_login': '2022-04-12T20:36:36.686Z',
        # 'last_name': 'Jermaine',
        self.assertEqual(user_data["last_name"], self.user.last_name)
        # 'organizations': [],
        self.assertEqual(user_data["organizations"], [])
        # 'teams': [],
        self.assertEqual(user_data["teams"], [])
        # 'time_zone': None,
        self.assertEqual(user_data["time_zone"], None)
        # 'username': 'zl2E6PrORKYwhVPfmepA50GGOlXzVQrEwHhudh0e0QPmB5beAz7dT6fw6bGPZ1op3G7kotuRqlRuH4P3LAXipnEYZqutO4WIgCTM'
        self.assertEqual(user_data["username"], self.user.username)
