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
from collaboration.models import ObjectSubscription, Comment, InboxItem


class TestSubscribeAndUnsubscribe(EventTestCase):
    def test_setting_subscribe_and_unsubscribe_works_for_frameworks(self):
        obj = Factory.framework(user=self.user)
        data = {
            "event_type": "subscribe",
            "object_type": "framework",
            "id": obj.ox_id,
        }

        self.assertEqual(ObjectSubscription.objects.count(), 0)
        self.resp_body = self.send_event(data)
        self.assertEqual(self.resp_body["success"], True)

        self.resp_body = self.resp_body["objs"]
        self.assertEqual(ObjectSubscription.objects.count(), 1)
        obj_data = self.get_nested_obj(f"window.aurochs.data.frameworks['{obj.ox_id}']")

        self.assertEqual(obj_data["subscribed"], True)

        data = {
            "event_type": "unsubscribe",
            "object_type": "framework",
            "id": obj.ox_id,
        }

        self.resp_body = self.send_event(data)

        self.assertEqual(self.resp_body["success"], True)
        self.resp_body = self.resp_body["objs"]
        obj_data = self.get_nested_obj(f"window.aurochs.data.frameworks['{obj.ox_id}']")

        self.assertEqual(ObjectSubscription.objects.count(), 0)
        self.assertEqual(obj_data["subscribed"], False)

    def test_setting_subscribe_and_unsubscribe_works_for_reports(self):
        obj = Factory.report(user=self.user)
        data = {
            "event_type": "subscribe",
            "object_type": "report",
            "id": obj.ox_id,
        }

        self.assertEqual(ObjectSubscription.objects.count(), 0)
        self.resp_body = self.send_event(data)

        self.assertEqual(self.resp_body["success"], True)
        self.resp_body = self.resp_body["objs"]
        self.assertEqual(ObjectSubscription.objects.count(), 1)
        obj_data = self.get_nested_obj(f"window.aurochs.data.reports['{obj.ox_id}']")

        self.assertEqual(obj_data["subscribed"], True)

        data = {
            "event_type": "unsubscribe",
            "object_type": "report",
            "id": obj.ox_id,
        }

        self.resp_body = self.send_event(data)

        self.assertEqual(self.resp_body["success"], True)
        self.resp_body = self.resp_body["objs"]
        obj_data = self.get_nested_obj(f"window.aurochs.data.reports['{obj.ox_id}']")

        self.assertEqual(ObjectSubscription.objects.count(), 0)
        self.assertEqual(obj_data["subscribed"], False)

    def test_setting_subscribe_and_unsubscribe_works_for_sources(self):
        obj = Factory.source(user=self.user)
        data = {
            "event_type": "subscribe",
            "object_type": "source",
            "id": obj.ox_id,
        }

        self.assertEqual(ObjectSubscription.objects.count(), 0)
        self.resp_body = self.send_event(data)

        self.assertEqual(self.resp_body["success"], True)
        self.resp_body = self.resp_body["objs"]
        self.assertEqual(ObjectSubscription.objects.count(), 1)
        obj_data = self.get_nested_obj(f"window.aurochs.data.sources['{obj.ox_id}']")

        self.assertEqual(obj_data["subscribed"], True)

        data = {
            "event_type": "unsubscribe",
            "object_type": "source",
            "id": obj.ox_id,
        }

        self.resp_body = self.send_event(data)

        self.assertEqual(self.resp_body["success"], True)
        self.resp_body = self.resp_body["objs"]
        obj_data = self.get_nested_obj(f"window.aurochs.data.sources['{obj.ox_id}']")

        self.assertEqual(ObjectSubscription.objects.count(), 0)
        self.assertEqual(obj_data["subscribed"], False)

    def test_setting_subscribe_and_unsubscribe_works_for_stacks(self):
        obj = Factory.stack(user=self.user)
        data = {
            "event_type": "subscribe",
            "object_type": "stack",
            "id": obj.ox_id,
        }

        self.assertEqual(ObjectSubscription.objects.count(), 0)
        self.resp_body = self.send_event(data)

        self.assertEqual(self.resp_body["success"], True)
        self.resp_body = self.resp_body["objs"]
        self.assertEqual(ObjectSubscription.objects.count(), 1)
        obj_data = self.get_nested_obj(f"window.aurochs.data.stacks['{obj.ox_id}']")

        self.assertEqual(obj_data["subscribed"], True)

        data = {
            "event_type": "unsubscribe",
            "object_type": "stack",
            "id": obj.ox_id,
        }

        self.resp_body = self.send_event(data)

        self.assertEqual(self.resp_body["success"], True)
        self.resp_body = self.resp_body["objs"]
        obj_data = self.get_nested_obj(f"window.aurochs.data.stacks['{obj.ox_id}']")

        self.assertEqual(ObjectSubscription.objects.count(), 0)
        self.assertEqual(obj_data["subscribed"], False)

    def test_subscribe_and_unsubscribe_are_not_allowed_for_object_without_view(self):
        obj = Factory.stack()
        data = {
            "event_type": "subscribe",
            "object_type": "stack",
            "id": obj.ox_id,
        }

        self.resp_body = self.send_event(data)
        self.assertEqual(ObjectSubscription.objects.count(), 0)
        self.assertEqual(self.resp_body["success"], False)

        data = {
            "event_type": "unsubscribe",
            "object_type": "stack",
            "id": obj.ox_id,
        }
        self.resp_body = self.send_event(data)
        self.assertEqual(ObjectSubscription.objects.count(), 0)
        self.assertEqual(self.resp_body["success"], False)

    def test_removing_user_permissions_also_removes_subscriptions_and_inbox(self):
        obj = Factory.stack(user=self.user)
        o = Factory.organization()
        u2, p2 = Factory.user(organization=o)
        o.add_user(self.user, can_manage=True, can_view=True)
        o.add_user(u2, can_manage=True, can_view=True)

        data = {
            "event_type": "subscribe",
            "object_type": "stack",
            "id": obj.ox_id,
        }

        self.assertEqual(ObjectSubscription.objects.count(), 0)
        self.resp_body = self.send_event(data)
        self.assertEqual(self.resp_body["success"], True)
        self.resp_body = self.resp_body["objs"]
        self.assertEqual(ObjectSubscription.objects.count(), 1)
        obj_data = self.get_nested_obj(f"window.aurochs.data.stacks['{obj.ox_id}']")
        self.assertEqual(obj_data["subscribed"], True)

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

        self.client.login(username=u2.username, password=p2)

        data = {
            "event_type": "add_comment",
            "object_type": "stack",
            "id": obj.ox_id,
            "body": Factory.rand_text(),
        }

        self.assertEqual(Comment.objects.count(), 0)
        self.resp_body = self.send_event(data)
        self.assertEqual(self.resp_body["success"], True)

        self.assertEqual(InboxItem.objects.count(), 1)
        self.assertEqual(Comment.objects.count(), 1)

        perm_list = [
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
        obj_data = self.get_nested_obj(f"window.aurochs.data.stacks['{obj.ox_id}']")

        self.assertEqual(ObjectSubscription.objects.count(), 0)
        self.assertEqual(InboxItem.objects.count(), 0)
        self.assertEqual(obj_data["subscribed"], False)

    def test_removing_user_from_org_also_removes_subscriptions_and_inbox(self):
        obj = Factory.stack(user=self.user)
        o = Factory.organization()
        u2, p2 = Factory.user(organization=o)
        o.add_user(self.user, can_manage=True, can_view=True)
        o.add_user(u2, can_manage=True, can_view=True)

        # Org owns the stack
        perm_list = [
            {
                "id": o.ox_id,
                "type": "organization",
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

        # Self.user subscribes
        data = {
            "event_type": "subscribe",
            "object_type": "stack",
            "id": obj.ox_id,
        }

        self.assertEqual(ObjectSubscription.objects.count(), 0)
        self.resp_body = self.send_event(data)
        self.assertEqual(self.resp_body["success"], True)

        self.resp_body = self.resp_body["objs"]
        self.assertEqual(ObjectSubscription.objects.count(), 1)
        self.assertEqual(ObjectSubscription.objects.all()[0].user, self.user)
        obj_data = self.get_nested_obj(f"window.aurochs.data.stacks['{obj.ox_id}']")
        self.assertEqual(obj_data["subscribed"], True)

        self.client.login(username=u2.username, password=p2)

        data = {
            "event_type": "add_comment",
            "object_type": "stack",
            "id": obj.ox_id,
            "body": Factory.rand_text(),
        }

        self.assertEqual(Comment.objects.count(), 0)
        self.resp_body = self.send_event(data)
        self.assertEqual(self.resp_body["success"], True)

        self.assertEqual(InboxItem.objects.count(), 1)
        self.assertEqual(Comment.objects.count(), 1)

        data = {
            "event_type": "update_organization",
            "id": o.ox_id,
            "name": Factory.rand_str(),
            "subtitle": Factory.rand_text(),
            "members": [
                # {"id": self.user.ox_id, "can_view": True, "can_manage": True},
                {"id": u2.ox_id, "can_view": True, "can_manage": True},
            ],
        }

        self.assertEqual(Organization.objects.all().count(), 1)
        self.assertEqual(OrganizationRole.objects.all().count(), 2)
        self.assertEqual(ObjectSubscription.objects.count(), 1)
        self.assertEqual(InboxItem.objects.count(), 1)

        # Remove self.user from the org.
        self.resp_body = self.send_event(data)
        self.assertEqual(self.resp_body["success"], True)

        self.assertEqual(Organization.objects.all().count(), 1)
        self.assertEqual(OrganizationRole.objects.all().count(), 1)

        self.assertEqual(ObjectSubscription.objects.count(), 0)
        self.assertEqual(InboxItem.objects.count(), 0)

    # When we want to enable tracking of changes on an item, uncomment these and .generate_history_change()es
    # def test_subscribe_and_changes_generates_inbox_items_for_frameworks(self):
    #     f = Factory.framework(user=self.user)
    #     data = {
    #         "event_type": "subscribe",
    #         "object_type": "framework",
    #         "id": f.ox_id,
    #     }

    #     self.assertEqual(ObjectSubscription.objects.count(), 0)
    #     self.resp_body = self.send_event(data)

    #     self.assertEqual(self.resp_body["success"], True)
    #     self.resp_body = self.resp_body["objs"]
    #     self.assertEqual(ObjectSubscription.objects.count(), 1)
    #     obj_data = self.get_nested_obj(f"window.aurochs.data.frameworks['{f.ox_id}']")

    #     self.assertEqual(obj_data["subscribed"], True)

    #     # Change the name.
    #     data = {
    #         "event_type": "update_framework",
    #         "id": f.ox_id,
    #         "name": Factory.rand_str(),
    #     }
    #     self.assertEqual(InboxItem.objects.count(), 0)
    #     self.resp_body = self.send_event(data)
    #     self.assertEqual(InboxItem.objects.count(), 1)
    #     ii = InboxItem.objects.all()[0]
    #     self.assertEqual(ii.user, self.user)
    #     self.assertEqual(ii.content_object, f)
    #     self.assertEqual(ii.change.change_type, "update_framework")

    #     user_data = self.get_nested_obj(f"window.aurochs.data.users['{self.user.ox_id}']")
    #     self.assertEqual(
    #         user_data["inbox"]["active"], [f"window.aurochs.data.inboxitems['{ii.ox_id}']"]
    #     )
    #     ii_data = self.get_nested_obj(f"window.aurochs.data.inboxitems['{ii.ox_id}']")
    #     self.assertEqual(ii_data["done"], False)
    #     self.assertEqual(ii_data["read"], False)
    #     self.assertEqual(ii_data["change_type"], "update_framework")
    #     self.assertEqual(
    #         ii_data["target"], f"window.aurochs.data.frameworks['{f.ox_id}']"
    #     )

    # def test_subscribe_and_changes_generates_inbox_items_for_reports(self):
    #     f = Factory.report(user=self.user)
    #     data = {
    #         "event_type": "subscribe",
    #         "object_type": "report",
    #         "id": f.ox_id,
    #     }

    #     self.assertEqual(ObjectSubscription.objects.count(), 0)
    #     self.resp_body = self.send_event(data)

    #     self.assertEqual(self.resp_body["success"], True)
    #     self.resp_body = self.resp_body["objs"]
    #     self.assertEqual(ObjectSubscription.objects.count(), 1)
    #     obj_data = self.get_nested_obj(f"window.aurochs.data.reports['{f.ox_id}']")

    #     self.assertEqual(obj_data["subscribed"], True)

    #     # Change the name.
    #     data = {
    #         "event_type": "update_report",
    #         "id": f.ox_id,
    #         "name": Factory.rand_str(),
    #     }
    #     self.assertEqual(InboxItem.objects.count(), 0)
    #     self.resp_body = self.send_event(data)
    #     self.assertEqual(InboxItem.objects.count(), 1)
    #     ii = InboxItem.objects.all()[0]
    #     self.assertEqual(ii.user, self.user)
    #     self.assertEqual(ii.content_object, f)
    #     self.assertEqual(ii.change.change_type, "update_report")

    #     user_data = self.get_nested_obj(f"window.aurochs.data.users['{self.user.ox_id}']")
    #     self.assertEqual(
    #         user_data["inbox"]["active"], [f"window.aurochs.data.inboxitems['{ii.ox_id}']"]
    #     )
    #     ii_data = self.get_nested_obj(f"window.aurochs.data.inboxitems['{ii.ox_id}']")
    #     self.assertEqual(ii_data["done"], False)
    #     self.assertEqual(ii_data["read"], False)
    #     self.assertEqual(ii_data["change_type"], "update_report")
    #     self.assertEqual(ii_data["target"], f"window.aurochs.data.reports['{f.ox_id}']")

    # def test_subscribe_and_changes_generates_inbox_items_for_sources(self):
    #     f = Factory.source(user=self.user)
    #     data = {
    #         "event_type": "subscribe",
    #         "object_type": "source",
    #         "id": f.ox_id,
    #     }

    #     self.assertEqual(ObjectSubscription.objects.count(), 0)
    #     self.resp_body = self.send_event(data)

    #     self.assertEqual(self.resp_body["success"], True)
    #     self.resp_body = self.resp_body["objs"]
    #     self.assertEqual(ObjectSubscription.objects.count(), 1)
    #     obj_data = self.get_nested_obj(f"window.aurochs.data.sources['{f.ox_id}']")

    #     self.assertEqual(obj_data["subscribed"], True)

    #     # Change the name.
    #     data = {
    #         "event_type": "update_source",
    #         "id": f.ox_id,
    #         "name": Factory.rand_str(),
    #     }
    #     self.assertEqual(InboxItem.objects.count(), 0)
    #     self.resp_body = self.send_event(data)
    #     self.assertEqual(InboxItem.objects.count(), 1)
    #     ii = InboxItem.objects.all()[0]
    #     self.assertEqual(ii.user, self.user)
    #     self.assertEqual(ii.content_object, f)
    #     self.assertEqual(ii.change.change_type, "update_source")

    #     user_data = self.get_nested_obj(f"window.aurochs.data.users['{self.user.ox_id}']")
    #     self.assertEqual(
    #         user_data["inbox"]["active"], [f"window.aurochs.data.inboxitems['{ii.ox_id}']"]
    #     )
    #     ii_data = self.get_nested_obj(f"window.aurochs.data.inboxitems['{ii.ox_id}']")
    #     self.assertEqual(ii_data["done"], False)
    #     self.assertEqual(ii_data["read"], False)
    #     self.assertEqual(ii_data["change_type"], "update_source")
    #     self.assertEqual(ii_data["target"], f"window.aurochs.data.sources['{f.ox_id}']")
