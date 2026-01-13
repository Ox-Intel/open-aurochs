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


class TestCreateFramework(EventTestCase):
    def test_endpoint(self):
        self.assertEqual(Framework.objects.count(), 0)
        f = Factory.framework(user=self.user)
        Factory.criteria(
            framework=f,
        )
        Factory.criteria(
            framework=f,
        )
        data = {
            "event_type": "clone_framework",
            "id": f.ox_id,
        }

        sent_time = self.now()
        self.resp_body = self.send_event(data)

        self.assertEqual(self.resp_body["success"], True)
        self.resp_body = self.resp_body["objs"]
        self.assertEqual(Framework.objects.all().count(), 2)
        f = Framework.objects.order_by("created_at").all()[0]
        f2 = Framework.objects.order_by("created_at").all()[1]

        self.assertEqual(f.name, f2.name)
        self.assertEqual(f.subtitle, f2.subtitle)

        self.assertEqual(f.criteria.count(), f2.criteria.count())
        self.assertEqual(f2.criteria.count(), 2)
        self.assertEqual(f2.parent, f)

        obj_data = self.get_nested_obj(f"window.aurochs.data.frameworks['{f2.ox_id}']")

        # Framework Data
        user_str = f"window.aurochs.data.users['{self.user.ox_id}']"
        # "window.aurochs.data.frameworks['1']": '{"__type": "framework",
        self.assertEqual(obj_data["__type"], "framework")

        self.assertEqual(
            obj_data["permissions"],
            {
                f"U-{self.user.ox_id}": "1111",
            },
        )
        self.assertEqual(f2.name, obj_data["name"])
        self.assertEqual(f2.subtitle, obj_data["subtitle"])

        # "created_at": "2022-04-12T19:18:30.437Z",
        self.assertBasicallyEqualTimes(
            datetime.fromtimestamp(int(obj_data["created_at_ms"]) / 1000), sent_time
        )
        # "created_at_ms": 1649791110437.731,
        # "created_by": user,
        self.assertEqual(obj_data["created_by"], user_str)

    def test_endpoint_with_data_change(self):
        self.assertEqual(Framework.objects.count(), 0)
        f = Factory.framework(user=self.user)
        Factory.criteria(
            framework=f,
        )
        Factory.criteria(
            framework=f,
        )
        data = {
            "event_type": "clone_framework",
            "id": f.ox_id,
            "name": Factory.rand_str(),
            "subtitle": Factory.rand_str(),
        }

        self.resp_body = self.send_event(data)

        self.assertEqual(self.resp_body["success"], True)
        self.resp_body = self.resp_body["objs"]
        self.assertEqual(Framework.objects.all().count(), 2)
        f = Framework.objects.order_by("created_at").all()[0]
        f2 = Framework.objects.order_by("created_at").all()[1]
        self.assertEqual(f2.parent, f)

        self.assertEqual(data["name"], f2.name)
        self.assertEqual(data["subtitle"], f2.subtitle)
