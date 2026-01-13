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
    GenericPermission,
)
from reports.models import Report, Scorecard, ScorecardScore
from sources.models import Source, SourceFeedback


class TestCreateTeam(EventTestCase):
    def test_team_admin_can_delete_team(self):
        o = Factory.organization()
        o.add_user(self.user, can_manage=True)
        t = Factory.team(organization=o)
        t.add_user(self.user, can_manage=True)

        self.assertEqual(Team.objects.all().count(), 1)
        self.assertEqual(TeamMember.objects.all().count(), 1)
        data = {"event_type": "delete_team", "id": t.ox_id}

        self.resp_body = self.send_event(data)

        self.assertEqual(self.resp_body["success"], True)
        self.resp_body = self.resp_body["objs"]
        self.assertEqual(Team.objects.all().count(), 0)
        self.assertEqual(TeamMember.objects.all().count(), 0)

    def test_org_admin_can_delete_team(self):
        o = Factory.organization()
        o.add_user(self.user, can_manage=True)
        t = Factory.team(organization=o)

        self.assertEqual(Team.objects.all().count(), 1)
        self.assertEqual(TeamMember.objects.all().count(), 0)
        data = {"event_type": "delete_team", "id": t.ox_id}

        self.resp_body = self.send_event(data)

        self.assertEqual(self.resp_body["success"], True)
        self.resp_body = self.resp_body["objs"]
        self.assertEqual(Team.objects.all().count(), 0)
        self.assertEqual(TeamMember.objects.all().count(), 0)

    def test_other_users_cannot_delete_team(self):
        o = Factory.organization()
        t = Factory.team(organization=o)

        self.assertEqual(Team.objects.all().count(), 1)
        self.assertEqual(TeamMember.objects.all().count(), 0)
        data = {"event_type": "delete_team", "id": t.ox_id}

        self.resp_body = self.send_event(data)

        self.assertEqual(self.resp_body["success"], False)
        self.assertEqual(Team.objects.all().count(), 1)

    def test_team_with_sole_content_cannot_be_deleted(self):
        o = Factory.organization()
        o.add_user(self.user, can_manage=True)
        t = Factory.team(organization=o)
        t.add_user(self.user)

        u2, p2 = Factory.user()
        f = Factory.framework(team=t, user=u2)
        f.remove_permission(acting_user=self.user, user=u2)

        self.assertEqual(GenericPermission.objects.all().count(), 1)

        data = {"event_type": "delete_team", "id": t.ox_id}

        self.resp_body = self.send_event(data)

        self.assertEqual(self.resp_body["success"], False)
        self.assertEqual(Team.objects.all().count(), 1)
        self.assertEqual(GenericPermission.objects.all().count(), 1)
