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


class TestUpdateStack(EventTestCase):
    def test_endpoint(self):
        obj = Factory.stack(user=self.user)
        data = {
            "event_type": "update_stack",
            "id": obj.ox_id,
            "name": Factory.rand_str(),
            "subtitle": Factory.rand_text(),
        }

        self.resp_body = self.send_event(data)

        self.assertEqual(self.resp_body["success"], True)
        self.resp_body = self.resp_body["objs"]
        self.assertEqual(Stack.objects.all().count(), 1)
        obj = Stack.objects.all()[0]
        self.assertEqual(obj.name, data["name"])
        self.assertEqual(obj.subtitle, data["subtitle"])

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
        # "created_at_ms": 1649791110437.731,
        # "created_by": user,
        self.assertEqual(obj_data["created_by"], user_str)
        # "deleted": false,

        # "deleted_at": null,

        # "subtitle": "Early.",
        self.assertEqual(obj_data["subtitle"], data["subtitle"])
        # "id": 1,
        self.assertEqual(obj_data["id"], obj.ox_id)
        # "modified_at": "2022-04-12T19:18:30.443Z",
        # "modified_at_ms": 1649791110443.849,
        # "modified_by": null,

        # "name": "R\\u2764\\ud83c\\udf81\\ud83d\\udc8cF\\u2642\\ud83c\\udfa7\\ud83c\\udf31Dl",
        self.assertEqual(obj_data["name"], data["name"])

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

    def test_add_report_to_stack(self):
        obj = Factory.stack(user=self.user)
        r = Factory.report(user=self.user)
        data = {
            "event_type": "add_report_to_stack",
            "stack_id": obj.ox_id,
            "report_id": r.ox_id,
            "name": Factory.rand_str(),
            "subtitle": Factory.rand_text(),
        }

        self.resp_body = self.send_event(data)

        self.assertEqual(self.resp_body["success"], True)
        self.resp_body = self.resp_body["objs"]
        self.assertEqual(Stack.objects.all().count(), 1)
        obj_data = self.get_nested_obj(f"window.aurochs.data.stacks['{obj.ox_id}']")
        obj = Stack.objects.all()[0]

        self.assertEqual(obj.reports.count(), 1)
        self.assertEqual(obj.reports.all()[0], r)

        self.assertEqual(
            obj_data["reports"],
            [
                f"window.aurochs.data.reports['{r.ox_id}']",
            ],
        )

    def test_remove_report_from_stack(self):
        obj = Factory.stack(user=self.user)
        r = Factory.report(user=self.user)
        data = {
            "event_type": "add_report_to_stack",
            "stack_id": obj.ox_id,
            "report_id": r.ox_id,
            "name": Factory.rand_str(),
            "subtitle": Factory.rand_text(),
        }

        self.resp_body = self.send_event(data)

        self.assertEqual(self.resp_body["success"], True)
        self.resp_body = self.resp_body["objs"]
        self.assertEqual(Stack.objects.all().count(), 1)
        obj = Stack.objects.all()[0]
        obj_data = self.get_nested_obj(f"window.aurochs.data.stacks['{obj.ox_id}']")

        self.assertEqual(obj.reports.count(), 1)
        self.assertEqual(obj.reports.all()[0], r)

        data = {
            "event_type": "remove_report_from_stack",
            "stack_id": obj.ox_id,
            "report_id": r.ox_id,
            "name": Factory.rand_str(),
            "subtitle": Factory.rand_text(),
        }

        self.resp_body = self.send_event(data)
        obj = Stack.objects.all()[0]
        obj_data = self.get_nested_obj(f"window.aurochs.data.stacks['{obj.ox_id}']")

        # 'username': 'zl2E6PrORKYwhVPfmepA50GGOlXzVQrEwHhudh0e0QPmB5beAz7dT6fw6bGPZ1op3G7kotuRqlRuH4P3LAXipnEYZqutO4WIgCTM'
        self.assertEqual(obj.reports.count(), 0)
        self.assertEqual(obj_data["reports"], [])
