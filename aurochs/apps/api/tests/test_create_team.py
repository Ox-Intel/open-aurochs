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
    Team,
    TeamMember,
)
from reports.models import Report, Scorecard, ScorecardScore
from sources.models import Source, SourceFeedback


class TestCreateTeam(EventTestCase):
    def test_create_team(self):
        o = Factory.organization()
        o.add_user(self.user, can_manage=True)
        data = {
            "event_type": "create_team",
            "name": Factory.rand_str(),
            "description": Factory.rand_text(),
            "org_id": o.ox_id,
        }

        self.resp_body = self.send_event(data)

        self.assertEqual(self.resp_body["success"], True)
        self.resp_body = self.resp_body["objs"]
        self.assertEqual(Team.objects.all().count(), 1)
        self.assertEqual(TeamMember.objects.all().count(), 1)
        obj = Team.objects.all()[0]
        self.assertEqual(obj.name, data["name"])
        self.assertEqual(obj.description, data["description"])

        obj_data = self.get_nested_obj(f"window.aurochs.data.teams['{obj.ox_id}']")
        self.assertEqual(obj_data["__type"], "team")

        self.assertEqual(obj_data["name"], data["name"])
        self.assertEqual(obj_data["description"], data["description"])
        self.assertEqual(
            obj_data["organization"], f"window.aurochs.data.organizations['{o.ox_id}']"
        )
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

    def test_create_team_not_allowed_outside_of_org(self):
        data = {
            "event_type": "create_team",
            "name": Factory.rand_str(),
            "description": Factory.rand_text(),
        }

        self.resp_body = self.send_event(data)

        self.assertEqual(self.resp_body["success"], False)
        self.assertEqual(Team.objects.all().count(), 0)
        self.assertEqual(TeamMember.objects.all().count(), 0)

    def test_create_team_allowed_as_non_admin(self):
        o = Factory.organization()
        o.add_user(self.user, can_manage=False)
        data = {
            "event_type": "create_team",
            "name": Factory.rand_str(),
            "description": Factory.rand_text(),
            "org_id": o.ox_id,
        }

        self.resp_body = self.send_event(data)

        self.assertEqual(self.resp_body["success"], True)
        self.assertEqual(Team.objects.all().count(), 1)
        self.assertEqual(TeamMember.objects.all().count(), 1)
        obj = Team.objects.all()[0]
        self.assertEqual(obj.name, data["name"])
        self.assertEqual(obj.description, data["description"])

        obj_data = self.get_nested_obj(f"window.aurochs.data.teams['{obj.ox_id}']")
        self.assertEqual(obj_data["__type"], "team")

        self.assertEqual(obj_data["name"], data["name"])
        self.assertEqual(obj_data["description"], data["description"])
        self.assertEqual(
            obj_data["organization"], f"window.aurochs.data.organizations['{o.ox_id}']"
        )
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
