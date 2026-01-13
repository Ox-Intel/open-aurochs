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
    User,
    Organization,
    OrganizationRole,
)
from reports.models import Report, Scorecard, ScorecardScore
from sources.models import Source, SourceFeedback


class TestCreateOrganization(EventTestCase):
    def test_create_organization(self):
        data = {
            "event_type": "create_organization",
            "name": Factory.rand_str(),
            "description": Factory.rand_text(),
        }

        self.resp_body = self.send_event(data)

        self.assertEqual(self.resp_body["success"], True)
        self.resp_body = self.resp_body["objs"]
        self.assertEqual(Organization.objects.all().count(), 1)
        obj = Organization.objects.all()[0]
        self.assertEqual(obj.name, data["name"])
        self.assertEqual(obj.description, data["description"])

        obj_data = self.get_nested_obj(
            f"window.aurochs.data.organizations['{obj.ox_id}']"
        )
        self.assertEqual(obj_data["__type"], "organization")

        self.assertEqual(obj_data["name"], data["name"])
        self.assertEqual(obj_data["description"], data["description"])
        self.assertEqual(obj_data["id"], obj.ox_id)
        self.assertEqual(
            obj_data["members"],
            [
                {
                    "id": self.user.ox_id,
                    "can_view": True,
                    "can_manage": True,
                },
            ],
        )
