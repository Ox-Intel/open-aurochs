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


class TestUpdateOrganization(EventTestCase):
    def test_update_organization_info_as_org_admin(self):
        o = Factory.organization()
        o.add_user(self.user, can_manage=True)

        data = {
            "event_type": "update_organization",
            "id": o.ox_id,
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

    def test_update_organization_info_as_not_organization_admin(self):
        o = Factory.organization()

        data = {
            "event_type": "update_organization",
            "id": o.ox_id,
            "name": Factory.rand_str(),
            "description": Factory.rand_text(),
        }

        self.resp_body = self.send_event(data)

        self.assertEqual(self.resp_body["success"], False)

    def test_update_organization_members(self):
        o = Factory.organization()
        o.add_user(self.user, can_manage=True)
        u2, p2 = Factory.user(organization=o)

        data = {
            "event_type": "update_organization",
            "id": o.ox_id,
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
        self.assertEqual(Organization.objects.all().count(), 1)
        self.assertEqual(OrganizationRole.objects.all().count(), 2)
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
                {
                    "id": u2.ox_id,
                    "can_view": True,
                    "can_manage": False,
                },
            ],
        )

        data = {
            "event_type": "update_organization",
            "id": o.ox_id,
            "name": Factory.rand_str(),
            "description": Factory.rand_text(),
            "members": [
                {"id": self.user.ox_id, "can_view": True, "can_manage": True},
            ],
        }

        self.resp_body = self.send_event(data)

        self.assertEqual(self.resp_body["success"], True)
        self.resp_body = self.resp_body["objs"]
        self.assertEqual(Organization.objects.all().count(), 1)
        self.assertEqual(OrganizationRole.objects.all().count(), 1)
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

    def test_not_allowed_to_break_organization_members(self):
        o = Factory.organization()
        o.add_user(self.user, can_manage=True)
        u2, p2 = Factory.user(organization=o)

        data = {
            "event_type": "update_organization",
            "id": o.ox_id,
            "name": Factory.rand_str(),
            "description": Factory.rand_text(),
            "members": [],
        }

        self.resp_body = self.send_event(data)

        self.assertEqual(self.resp_body["success"], False)
        self.assertEqual(Organization.objects.all().count(), 1)
        self.assertEqual(OrganizationRole.objects.all().count(), 2)

        data = {
            "event_type": "update_organization",
            "id": o.ox_id,
            "name": Factory.rand_str(),
            "description": Factory.rand_text(),
            "members": [
                {"id": self.user.ox_id, "can_view": True, "can_manage": False},
            ],
        }

        self.resp_body = self.send_event(data)

        self.assertEqual(self.resp_body["success"], False)
        self.assertEqual(Organization.objects.all().count(), 1)
        self.assertEqual(OrganizationRole.objects.all().count(), 2)

    def test_can_change_organization_ownership(self):
        o = Factory.organization()
        o.add_user(self.user, can_manage=True)
        u2, p2 = Factory.user(organization=o)

        data = {
            "event_type": "update_organization",
            "id": o.ox_id,
            "name": Factory.rand_str(),
            "description": Factory.rand_text(),
            "members": [
                {"id": u2.ox_id, "can_view": True, "can_manage": True},
            ],
        }

        self.resp_body = self.send_event(data)

        self.assertEqual(self.resp_body["success"], True)
        self.assertEqual(Organization.objects.all().count(), 1)
        self.assertEqual(OrganizationRole.objects.all().count(), 1)
        self.assertEqual(OrganizationRole.objects.all()[0].user, u2)
        self.assertEqual(OrganizationRole.objects.all()[0].can_view, True)
        self.assertEqual(OrganizationRole.objects.all()[0].can_manage, True)

    def test_removing_an_org_member_also_removes_them_from_all_org_teams(self):
        o = Factory.organization()
        o.add_user(self.user, can_manage=True)
        t1 = Factory.team(organization=o)
        t2 = Factory.team(organization=o)
        u2, p2 = Factory.user()
        o.add_user(u2, can_manage=True)

        data = {
            "event_type": "update_organization",
            "id": o.ox_id,
            "name": Factory.rand_str(),
            "description": Factory.rand_text(),
            "members": [
                {"id": self.user.ox_id, "can_view": True, "can_manage": True},
                {"id": u2.ox_id, "can_view": True, "can_manage": True},
            ],
        }
        self.resp_body = self.send_event(data)
        self.assertEqual(self.resp_body["success"], True)
        self.assertEqual(Organization.objects.all().count(), 1)
        self.assertEqual(OrganizationRole.objects.all().count(), 2)

        data = {
            "event_type": "update_team",
            "id": t1.ox_id,
            "members": [
                {"id": self.user.ox_id, "can_view": True, "can_manage": True},
                {"id": u2.ox_id, "can_view": True, "can_manage": True},
            ],
        }
        self.resp_body = self.send_event(data)
        self.assertEqual(self.resp_body["success"], True)
        self.assertEqual(Team.objects.all().count(), 2)
        self.assertEqual(len(Team.objects.all()[0].members), 2)
        self.assertEqual(Team.objects.all()[0].members[0], self.user)
        self.assertEqual(Team.objects.all()[0].members[1], u2)

        data = {
            "event_type": "update_team",
            "id": t2.ox_id,
            "members": [
                {"id": self.user.ox_id, "can_view": True, "can_manage": True},
                {"id": u2.ox_id, "can_view": True, "can_manage": True},
            ],
        }
        self.resp_body = self.send_event(data)
        self.assertEqual(self.resp_body["success"], True)
        self.assertEqual(Team.objects.all().count(), 2)
        self.assertEqual(len(Team.objects.all()[1].members), 2)
        self.assertEqual(Team.objects.all()[1].members[0], self.user)
        self.assertEqual(Team.objects.all()[1].members[1], u2)

        data = {
            "event_type": "update_organization",
            "id": o.ox_id,
            "name": Factory.rand_str(),
            "description": Factory.rand_text(),
            "members": [
                {"id": self.user.ox_id, "can_view": True, "can_manage": True},
            ],
        }
        self.resp_body = self.send_event(data)
        self.assertEqual(self.resp_body["success"], True)
        self.assertEqual(Organization.objects.all().count(), 1)

        self.assertEqual(Team.objects.all().count(), 2)
        self.assertEqual(len(Team.objects.all()[0].members), 1)
        self.assertEqual(len(Team.objects.all()[1].members), 1)

        self.client.login(username=u2.username, password=p2)

        data = {
            "event_type": "get_my_user",
        }
        self.resp_body = self.send_event(data)
        user_str = f"window.aurochs.data.users['{u2.ox_id}']"
        user_data = self.get_nested_obj(user_str)
        self.assertEqual(user_data["teams"], [])
