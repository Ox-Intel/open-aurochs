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
from stacks.models import Stack


class TestDeleteStack(EventTestCase):
    def test_endpoint(self):
        self.assertEqual(Stack.objects.count(), 0)
        obj = Factory.stack(user=self.user)
        self.assertEqual(Stack.objects.count(), 1)

        data = {
            "event_type": "delete_stack",
            "id": obj.ox_id,
        }

        # sent_time = self.now()
        self.resp_body = self.send_event(data)

        self.assertEqual(self.resp_body["success"], True)
        self.resp_body = self.resp_body["objs"]
        self.assertEqual(Stack.objects.count(), 0)


class TestDeleteStackAsTeam(EventTestCase):
    def test_in_team_deletes(self):
        self.assertEqual(Stack.objects.count(), 0)
        o = Factory.organization()
        o.add_user(self.user)
        t = Factory.team(organization=o)
        t.add_user(self.user)

        r = Factory.stack(team=t)
        self.assertEqual(Stack.objects.count(), 1)

        data = {
            "event_type": "delete_stack",
            "id": r.ox_id,
        }

        # sent_time = self.now()
        self.resp_body = self.send_event(data)

        self.assertEqual(self.resp_body["success"], True)
        self.resp_body = self.resp_body["objs"]
        self.assertEqual(Stack.objects.count(), 0)

    def test_not_in_team_does_not_delete(self):
        self.assertEqual(Stack.objects.count(), 0)
        o = Factory.organization()
        # o.add_user(self.user)
        t = Factory.team(organization=o)
        # t.add_user(self.user)

        r = Factory.stack(team=t)
        self.assertEqual(Stack.objects.count(), 1)

        data = {
            "event_type": "delete_stack",
            "id": r.ox_id,
        }

        # sent_time = self.now()
        self.resp_body = self.send_event(data)

        self.assertEqual(self.resp_body["success"], False)
        self.assertEqual(Stack.objects.count(), 1)


class TestDeleteStackAsOrg(EventTestCase):
    def test_in_org_deletes(self):
        self.assertEqual(Stack.objects.count(), 0)
        o = Factory.organization()
        o.add_user(self.user)

        r = Factory.stack(organization=o)
        self.assertEqual(Stack.objects.count(), 1)

        data = {
            "event_type": "delete_stack",
            "id": r.ox_id,
        }

        # sent_time = self.now()
        self.resp_body = self.send_event(data)

        self.assertEqual(self.resp_body["success"], True)
        self.resp_body = self.resp_body["objs"]
        self.assertEqual(Stack.objects.count(), 0)

    def test_not_in_org_does_not_delete(self):
        self.assertEqual(Stack.objects.count(), 0)
        o = Factory.organization()
        # o.add_user(self.user)
        # t = Factory.team(organization=o)
        # t.add_user(self.user)

        r = Factory.stack(organization=o)
        self.assertEqual(Stack.objects.count(), 1)

        data = {
            "event_type": "delete_stack",
            "id": r.ox_id,
        }

        # sent_time = self.now()
        self.resp_body = self.send_event(data)

        self.assertEqual(self.resp_body["success"], False)
        self.assertEqual(Stack.objects.count(), 1)
