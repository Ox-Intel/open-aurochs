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


class TestUpdateTeam(EventTestCase):
    def test_update_team_info_as_org_admin(self):
        o = Factory.organization()
        o.add_user(self.user, can_manage=True)
        team = Factory.team(organization=o)
        team.add_user(self.user)

        data = {
            "event_type": "update_team",
            "id": team.ox_id,
            "name": Factory.rand_str(),
            "description": Factory.rand_text(),
        }

        self.resp_body = self.send_event(data)

        self.assertEqual(self.resp_body["success"], True)
        self.resp_body = self.resp_body["objs"]
        self.assertEqual(Team.objects.all().count(), 1)
        obj = Team.objects.all()[0]
        self.assertEqual(obj.name, data["name"])
        self.assertEqual(obj.description, data["description"])

        obj_data = self.get_nested_obj(f"window.aurochs.data.teams['{obj.ox_id}']")
        self.assertEqual(obj_data["__type"], "team")

        self.assertEqual(obj_data["name"], data["name"])
        self.assertEqual(obj_data["description"], data["description"])
        self.assertEqual(obj_data["id"], obj.ox_id)
        self.assertEqual(
            obj_data["members"],
            [
                {
                    "id": self.user.ox_id,
                    "can_view": True,
                    "can_manage": False,
                },
            ],
        )

    def test_update_team_info_as_team_admin(self):
        o = Factory.organization()
        o.add_user(self.user)
        team = Factory.team(organization=o)
        team.add_user(self.user, can_manage=True)

        data = {
            "event_type": "update_team",
            "id": team.ox_id,
            "name": Factory.rand_str(),
            "description": Factory.rand_text(),
        }

        self.resp_body = self.send_event(data)

        self.assertEqual(self.resp_body["success"], True)
        self.resp_body = self.resp_body["objs"]
        self.assertEqual(Team.objects.all().count(), 1)
        obj = Team.objects.all()[0]
        self.assertEqual(obj.name, data["name"])
        self.assertEqual(obj.description, data["description"])

        obj_data = self.get_nested_obj(f"window.aurochs.data.teams['{obj.ox_id}']")
        self.assertEqual(obj_data["__type"], "team")

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

    def test_update_team_members(self):
        o = Factory.organization()
        o.add_user(self.user, can_manage=True)
        u2, p2 = Factory.user(organization=o)
        team = Factory.team(organization=o)
        team.add_user(self.user)

        data = {
            "event_type": "update_team",
            "id": team.ox_id,
            "name": Factory.rand_str(),
            "description": Factory.rand_text(),
            "members": [
                {"id": self.user.ox_id, "can_view": True, "can_manage": True},
                {"id": u2.ox_id, "can_view": True, "can_manage": False},
            ],
        }

        self.resp_body = self.send_event(data)

        self.assertEqual(self.resp_body["success"], True)
        self.resp_body = self.resp_body["objs"]
        self.assertEqual(Team.objects.all().count(), 1)
        self.assertEqual(TeamMember.objects.all().count(), 2)
        obj = Team.objects.all()[0]
        self.assertEqual(obj.name, data["name"])
        self.assertEqual(obj.description, data["description"])

        obj_data = self.get_nested_obj(f"window.aurochs.data.teams['{obj.ox_id}']")
        self.assertEqual(obj_data["__type"], "team")

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
                {
                    "id": u2.ox_id,
                    "can_view": True,
                    "can_manage": False,
                },
            ],
        )

        data = {
            "event_type": "update_team",
            "id": team.ox_id,
            "name": Factory.rand_str(),
            "description": Factory.rand_text(),
            "members": [
                {"id": self.user.ox_id, "can_view": True, "can_manage": True},
            ],
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

    def test_not_allowed_to_break_team_members(self):
        o = Factory.organization()
        o.add_user(self.user, can_manage=True)
        u2, p2 = Factory.user(organization=o)
        team = Factory.team(organization=o)
        team.add_user(self.user)

        data = {
            "event_type": "update_team",
            "id": team.ox_id,
            "name": Factory.rand_str(),
            "description": Factory.rand_text(),
            "members": [],
        }

        self.resp_body = self.send_event(data)

        self.assertEqual(self.resp_body["success"], True)
        self.assertEqual(Team.objects.all().count(), 1)
        self.assertEqual(TeamMember.objects.all().count(), 0)

        data = {
            "event_type": "update_team",
            "id": team.ox_id,
            "name": Factory.rand_str(),
            "description": Factory.rand_text(),
            "members": [
                {"id": self.user.ox_id, "can_view": True, "can_manage": False},
            ],
        }

        self.resp_body = self.send_event(data)

        self.assertEqual(self.resp_body["success"], True)
        self.assertEqual(Team.objects.all().count(), 1)
        self.assertEqual(TeamMember.objects.all().count(), 1)

    def test_can_change_team_ownership(self):
        o = Factory.organization()
        o.add_user(self.user, can_manage=True)
        u2, p2 = Factory.user(organization=o)
        team = Factory.team(organization=o)
        team.add_user(self.user)

        data = {
            "event_type": "update_team",
            "id": team.ox_id,
            "name": Factory.rand_str(),
            "description": Factory.rand_text(),
            "members": [
                {"id": u2.ox_id, "can_view": True, "can_manage": True},
            ],
        }

        self.resp_body = self.send_event(data)

        self.assertEqual(self.resp_body["success"], True)
        self.assertEqual(Team.objects.all().count(), 1)
        self.assertEqual(TeamMember.objects.all().count(), 1)
        self.assertEqual(TeamMember.objects.all()[0].user, u2)
        self.assertEqual(TeamMember.objects.all()[0].can_view, True)
        self.assertEqual(TeamMember.objects.all()[0].can_manage, True)
