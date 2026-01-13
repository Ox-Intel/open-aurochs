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


class TestCreateUser(EventTestCase):
    def test_endpoint(self):
        o = Factory.organization()
        o.add_user(self.user, can_manage=True, can_view=True)
        self.assertEqual(User.objects.count(), 1)
        data = {
            "event_type": "create_user",
            "first_name": Factory.rand_str(),
            "last_name": Factory.rand_str(),
            "email": Factory.rand_email(),
            "username": Factory.rand_email(),
            "password": Factory.rand_str(),
            "org_id": o.ox_id,
        }

        self.resp_body = self.send_event(data)

        self.assertEqual(self.resp_body["success"], True)
        self.resp_body = self.resp_body["objs"]
        self.assertEqual(User.objects.all().count(), 2)
        obj = User.objects.all().order_by("created_at")[1]
        self.assertEqual(obj.first_name, data["first_name"])
        self.assertEqual(obj.last_name, data["last_name"])
        self.assertEqual(obj.email, data["email"])
        self.assertEqual(obj.username, data["username"])
        self.assertTrue(obj.check_password(data["password"]))

        obj_data = self.get_nested_obj(f"window.aurochs.data.users['{obj.ox_id}']")

        self.assertEqual(obj_data["__type"], "user")
        self.assertEqual(obj_data["first_name"], data["first_name"])
        self.assertEqual(obj_data["last_name"], data["last_name"])
        self.assertEqual(
            obj_data["full_name"], f'{data["first_name"]} {data["last_name"]}'
        )
        self.assertEqual(obj_data["id"], obj.ox_id)

        # self.assertEqual(
        #     obj_data["organizations"],
        #     [f"window.aurochs.data.organizations['{o.ox_id}']"],
        # )
        # self.assertEqual(obj_data["teams"], [])

    def test_username_available(self):
        data = {
            "event_type": "check_username",
            "username": Factory.rand_str(),
        }

        self.resp_body = self.send_event(data)
        self.assertEqual(self.resp_body["success"], True)
        self.assertEqual(self.resp_body["available"], True)

        data = {
            "event_type": "check_username",
            "username": self.user.username,
        }

        self.resp_body = self.send_event(data)
        self.assertEqual(self.resp_body["success"], True)
        self.assertEqual(self.resp_body["available"], False)
