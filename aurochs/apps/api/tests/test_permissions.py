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
    Tag,
    TaggedObject,
)
from reports.models import Report, Scorecard, ScorecardScore
from sources.models import Source, SourceFeedback
from stacks.models import Stack
from collaboration.models import ObjectSubscription, Comment, InboxItem


class TestEditPermissions(EventTestCase):
    def test_setting_permissions_on_frameworks(self):
        obj = Factory.framework(user=self.user)
        u2, p2 = Factory.user()
        self.assertTrue(obj.can_score(user=self.user))
        self.assertTrue(obj.can_read(user=self.user))
        self.assertTrue(obj.can_write(user=self.user))
        self.assertTrue(obj.can_administer(user=self.user))
        self.assertFalse(obj.can_score(user=u2))
        self.assertFalse(obj.can_read(user=u2))
        self.assertFalse(obj.can_write(user=u2))
        self.assertFalse(obj.can_administer(user=u2))

        perm_list = [
            {
                "id": self.user.ox_id,
                "type": "user",
                "score": True,
                "read": True,
                "write": True,
                "administer": True,
            },
            {
                "id": u2.ox_id,
                "type": "user",
                "score": True,
                "read": True,
                "write": True,
                "administer": True,
            },
        ]
        data = {
            "event_type": "update_permissions",
            "type": "framework",
            "id": obj.ox_id,
            "permissions": perm_list,
        }
        self.resp_body = self.send_event(data)
        self.assertEqual(self.resp_body["success"], True)

        self.resp_body = self.resp_body["objs"]
        obj = Framework.objects.get(pk=obj.pk)
        self.assertTrue(obj.can_score(user=self.user))
        self.assertTrue(obj.can_read(user=self.user))
        self.assertTrue(obj.can_write(user=self.user))
        self.assertTrue(obj.can_administer(user=self.user))
        self.assertTrue(obj.can_score(user=u2))
        self.assertTrue(obj.can_read(user=u2))
        self.assertTrue(obj.can_write(user=u2))
        self.assertTrue(obj.can_administer(user=u2))

    def test_setting_permissions_on_reports(self):
        obj = Factory.report(user=self.user)
        u2, p2 = Factory.user()
        self.assertTrue(obj.can_score(user=self.user))
        self.assertTrue(obj.can_read(user=self.user))
        self.assertTrue(obj.can_write(user=self.user))
        self.assertTrue(obj.can_administer(user=self.user))
        self.assertFalse(obj.can_score(user=u2))
        self.assertFalse(obj.can_read(user=u2))
        self.assertFalse(obj.can_write(user=u2))
        self.assertFalse(obj.can_administer(user=u2))

        perm_list = [
            {
                "id": self.user.ox_id,
                "type": "user",
                "score": True,
                "read": True,
                "write": True,
                "administer": True,
            },
            {
                "id": u2.ox_id,
                "type": "user",
                "score": True,
                "read": True,
                "write": True,
                "administer": True,
            },
        ]
        data = {
            "event_type": "update_permissions",
            "type": "report",
            "id": obj.ox_id,
            "permissions": perm_list,
        }
        self.resp_body = self.send_event(data)
        self.assertEqual(self.resp_body["success"], True)

        self.resp_body = self.resp_body["objs"]
        obj = Report.objects.get(pk=obj.pk)
        self.assertTrue(obj.can_score(user=self.user))
        self.assertTrue(obj.can_read(user=self.user))
        self.assertTrue(obj.can_write(user=self.user))
        self.assertTrue(obj.can_administer(user=self.user))
        self.assertTrue(obj.can_score(user=u2))
        self.assertTrue(obj.can_read(user=u2))
        self.assertTrue(obj.can_write(user=u2))
        self.assertTrue(obj.can_administer(user=u2))

    def test_setting_permissions_on_sources(self):
        obj = Factory.source(user=self.user)
        u2, p2 = Factory.user()
        self.assertTrue(obj.can_score(user=self.user))
        self.assertTrue(obj.can_read(user=self.user))
        self.assertTrue(obj.can_write(user=self.user))
        self.assertTrue(obj.can_administer(user=self.user))
        self.assertFalse(obj.can_score(user=u2))
        self.assertFalse(obj.can_read(user=u2))
        self.assertFalse(obj.can_write(user=u2))
        self.assertFalse(obj.can_administer(user=u2))

        perm_list = [
            {
                "id": self.user.ox_id,
                "type": "user",
                "score": True,
                "read": True,
                "write": True,
                "administer": True,
            },
            {
                "id": u2.ox_id,
                "type": "user",
                "score": True,
                "read": True,
                "write": True,
                "administer": True,
            },
        ]
        data = {
            "event_type": "update_permissions",
            "type": "source",
            "id": obj.ox_id,
            "permissions": perm_list,
        }
        self.resp_body = self.send_event(data)
        self.assertEqual(self.resp_body["success"], True)

        self.resp_body = self.resp_body["objs"]
        obj = Source.objects.get(pk=obj.pk)
        self.assertTrue(obj.can_score(user=self.user))
        self.assertTrue(obj.can_read(user=self.user))
        self.assertTrue(obj.can_write(user=self.user))
        self.assertTrue(obj.can_administer(user=self.user))
        self.assertTrue(obj.can_score(user=u2))
        self.assertTrue(obj.can_read(user=u2))
        self.assertTrue(obj.can_write(user=u2))
        self.assertTrue(obj.can_administer(user=u2))

    def test_setting_permissions_on_stacks(self):
        obj = Factory.stack(user=self.user)
        u2, p2 = Factory.user()
        self.assertTrue(obj.can_score(user=self.user))
        self.assertTrue(obj.can_read(user=self.user))
        self.assertTrue(obj.can_write(user=self.user))
        self.assertTrue(obj.can_administer(user=self.user))
        self.assertFalse(obj.can_score(user=u2))
        self.assertFalse(obj.can_read(user=u2))
        self.assertFalse(obj.can_write(user=u2))
        self.assertFalse(obj.can_administer(user=u2))

        perm_list = [
            {
                "id": self.user.ox_id,
                "type": "user",
                "score": True,
                "read": True,
                "write": True,
                "administer": True,
            },
            {
                "id": u2.ox_id,
                "type": "user",
                "score": True,
                "read": True,
                "write": True,
                "administer": True,
            },
        ]
        data = {
            "event_type": "update_permissions",
            "type": "stack",
            "id": obj.ox_id,
            "permissions": perm_list,
        }
        self.resp_body = self.send_event(data)
        self.assertEqual(self.resp_body["success"], True)

        self.resp_body = self.resp_body["objs"]
        obj = Stack.objects.get(pk=obj.pk)
        self.assertTrue(obj.can_score(user=self.user))
        self.assertTrue(obj.can_read(user=self.user))
        self.assertTrue(obj.can_write(user=self.user))
        self.assertTrue(obj.can_administer(user=self.user))
        self.assertTrue(obj.can_score(user=u2))
        self.assertTrue(obj.can_read(user=u2))
        self.assertTrue(obj.can_write(user=u2))
        self.assertTrue(obj.can_administer(user=u2))

    def test_cannot_remove_last_permissions(self):
        # Not allowed to remove last.
        obj = Factory.source(user=self.user)
        u2, p2 = Factory.user()

        perm_list = [
            {
                "id": self.user.ox_id,
                "type": "user",
                "score": False,
                "read": False,
                "write": False,
                "administer": False,
            },
        ]
        data = {
            "event_type": "update_permissions",
            "type": "source",
            "id": obj.ox_id,
            "permissions": perm_list,
        }
        self.resp_body = self.send_event(data)
        self.assertEqual(self.resp_body["success"], False)

    def test_can_set_last_permissions_to_someone_else(self):
        obj = Factory.source(user=self.user)
        u2, p2 = Factory.user()
        self.assertTrue(obj.can_score(user=self.user))
        self.assertTrue(obj.can_read(user=self.user))
        self.assertTrue(obj.can_write(user=self.user))
        self.assertTrue(obj.can_administer(user=self.user))
        self.assertFalse(obj.can_score(user=u2))
        self.assertFalse(obj.can_read(user=u2))
        self.assertFalse(obj.can_write(user=u2))
        self.assertFalse(obj.can_administer(user=u2))

        perm_list = [
            {
                "id": self.user.ox_id,
                "type": "user",
                "score": False,
                "read": False,
                "write": False,
                "administer": False,
            },
            {
                "id": u2.ox_id,
                "type": "user",
                "score": True,
                "read": True,
                "write": True,
                "administer": True,
            },
        ]
        data = {
            "event_type": "update_permissions",
            "type": "source",
            "id": obj.ox_id,
            "permissions": perm_list,
        }
        self.resp_body = self.send_event(data)
        self.assertEqual(self.resp_body["success"], True)

        self.resp_body = self.resp_body["objs"]
        obj = Source.objects.get(pk=obj.pk)
        self.assertFalse(obj.can_score(user=self.user))
        self.assertFalse(obj.can_read(user=self.user))
        self.assertFalse(obj.can_write(user=self.user))
        self.assertFalse(obj.can_administer(user=self.user))
        self.assertTrue(obj.can_score(user=u2))
        self.assertTrue(obj.can_read(user=u2))
        self.assertTrue(obj.can_write(user=u2))
        self.assertTrue(obj.can_administer(user=u2))

        # Now should error because I don't have admin permissions.
        self.resp_body = self.send_event(data)
        self.assertEqual(self.resp_body["success"], False)

    def test_setting_permissions_to_teams(self):
        obj = Factory.source(user=self.user)
        t1 = Factory.team()
        self.assertTrue(obj.can_score(user=self.user))
        self.assertTrue(obj.can_read(user=self.user))
        self.assertTrue(obj.can_write(user=self.user))
        self.assertTrue(obj.can_administer(user=self.user))
        self.assertFalse(obj.can_score(team=t1))
        self.assertFalse(obj.can_read(team=t1))
        self.assertFalse(obj.can_write(team=t1))
        self.assertFalse(obj.can_administer(team=t1))

        perm_list = [
            {
                "id": self.user.ox_id,
                "type": "user",
                "score": True,
                "read": True,
                "write": True,
                "administer": True,
            },
            {
                "id": t1.ox_id,
                "type": "team",
                "score": True,
                "read": True,
                "write": True,
                "administer": True,
            },
        ]
        data = {
            "event_type": "update_permissions",
            "type": "source",
            "id": obj.ox_id,
            "permissions": perm_list,
        }
        self.resp_body = self.send_event(data)
        self.assertEqual(self.resp_body["success"], True)

        self.resp_body = self.resp_body["objs"]
        obj = Source.objects.get(ox_id=obj.ox_id)
        self.assertTrue(obj.can_score(user=self.user))
        self.assertTrue(obj.can_read(user=self.user))
        self.assertTrue(obj.can_write(user=self.user))
        self.assertTrue(obj.can_administer(user=self.user))
        self.assertTrue(obj.can_score(team=t1))
        self.assertTrue(obj.can_read(team=t1))
        self.assertTrue(obj.can_write(team=t1))
        self.assertTrue(obj.can_administer(team=t1))

    def test_setting_permissions_to_orgs(self):
        obj = Factory.source(user=self.user)
        o2 = Factory.organization()
        self.assertTrue(obj.can_score(user=self.user))
        self.assertTrue(obj.can_read(user=self.user))
        self.assertTrue(obj.can_write(user=self.user))
        self.assertTrue(obj.can_administer(user=self.user))
        self.assertFalse(obj.can_score(organization=o2))
        self.assertFalse(obj.can_read(organization=o2))
        self.assertFalse(obj.can_write(organization=o2))
        self.assertFalse(obj.can_administer(organization=o2))

        perm_list = [
            {
                "id": self.user.ox_id,
                "type": "user",
                "score": True,
                "read": True,
                "write": True,
                "administer": True,
            },
            {
                "id": o2.ox_id,
                "type": "organization",
                "score": True,
                "read": True,
                "write": True,
                "administer": True,
            },
        ]
        data = {
            "event_type": "update_permissions",
            "type": "source",
            "id": obj.ox_id,
            "permissions": perm_list,
        }
        self.resp_body = self.send_event(data)
        self.assertEqual(self.resp_body["success"], True)

        self.resp_body = self.resp_body["objs"]
        obj = Source.objects.get(pk=obj.pk)
        self.assertTrue(obj.can_score(user=self.user))
        self.assertTrue(obj.can_read(user=self.user))
        self.assertTrue(obj.can_write(user=self.user))
        self.assertTrue(obj.can_administer(user=self.user))
        self.assertTrue(obj.can_score(organization=o2))
        self.assertTrue(obj.can_read(organization=o2))
        self.assertTrue(obj.can_write(organization=o2))
        self.assertTrue(obj.can_administer(organization=o2))

    def test_edit_permission_cascades_to_read_and_score(self):
        obj = Factory.source(user=self.user)
        u2, p2 = Factory.user()
        self.assertTrue(obj.can_score(user=self.user))
        self.assertTrue(obj.can_read(user=self.user))
        self.assertTrue(obj.can_write(user=self.user))
        self.assertTrue(obj.can_administer(user=self.user))

        # Need to use a second user.
        self.assertFalse(obj.can_score(user=u2))
        self.assertFalse(obj.can_read(user=u2))
        self.assertFalse(obj.can_write(user=u2))
        self.assertFalse(obj.can_administer(user=u2))

        perm_list = [
            {
                "id": self.user.ox_id,
                "type": "user",
                "score": True,
                "read": True,
                "write": True,
                "administer": True,
            },
            {
                "id": u2.ox_id,
                "type": "user",
                "score": False,
                "read": False,
                "write": True,
                "administer": False,
            },
        ]
        data = {
            "event_type": "update_permissions",
            "type": "source",
            "id": obj.ox_id,
            "permissions": perm_list,
        }
        self.resp_body = self.send_event(data)
        self.assertEqual(self.resp_body["success"], True)

        self.resp_body = self.resp_body["objs"]
        obj = Source.objects.get(pk=obj.pk)
        self.assertTrue(obj.can_score(user=u2))
        self.assertTrue(obj.can_read(user=u2))
        self.assertTrue(obj.can_write(user=u2))
        self.assertFalse(obj.can_administer(user=u2))

    def test_admin_permission_cascades_to_read_and_score(self):
        obj = Factory.source(user=self.user)
        self.assertTrue(obj.can_score(user=self.user))
        self.assertTrue(obj.can_read(user=self.user))
        self.assertTrue(obj.can_write(user=self.user))
        self.assertTrue(obj.can_administer(user=self.user))

        perm_list = [
            {
                "id": self.user.ox_id,
                "type": "user",
                "score": False,
                "read": False,
                "write": False,
                "administer": True,
            },
        ]
        data = {
            "event_type": "update_permissions",
            "type": "source",
            "id": obj.ox_id,
            "permissions": perm_list,
        }
        self.resp_body = self.send_event(data)
        self.assertEqual(self.resp_body["success"], True)

        self.resp_body = self.resp_body["objs"]
        obj = Source.objects.get(pk=obj.pk)
        self.assertTrue(obj.can_score(user=self.user))
        self.assertTrue(obj.can_read(user=self.user))
        self.assertTrue(obj.can_write(user=self.user))
        self.assertTrue(obj.can_administer(user=self.user))

        # Also checking with second user.
        u2, p2 = Factory.user()
        self.assertFalse(obj.can_score(user=u2))
        self.assertFalse(obj.can_read(user=u2))
        self.assertFalse(obj.can_write(user=u2))
        self.assertFalse(obj.can_administer(user=u2))

        perm_list = [
            {
                "id": u2.ox_id,
                "type": "user",
                "score": False,
                "read": False,
                "write": False,
                "administer": True,
            },
        ]
        data = {
            "event_type": "update_permissions",
            "type": "source",
            "id": obj.ox_id,
            "permissions": perm_list,
        }
        self.resp_body = self.send_event(data)
        self.assertEqual(self.resp_body["success"], True)

        self.resp_body = self.resp_body["objs"]
        obj = Source.objects.get(pk=obj.pk)
        self.assertTrue(obj.can_score(user=u2))
        self.assertTrue(obj.can_read(user=u2))
        self.assertTrue(obj.can_write(user=u2))
        self.assertTrue(obj.can_administer(user=u2))
