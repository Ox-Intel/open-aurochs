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
from history.models import ObjectHistoryChange


class TestCommenting(EventTestCase):
    def tearDown(self):
        self.client.login(username=self.user.username, password=self.password)

    def test_add_edit_and_delete_on_framework(self):
        obj = Factory.framework(user=self.user)
        data = {
            "event_type": "add_comment",
            "object_type": "framework",
            "id": obj.ox_id,
            "body": Factory.rand_text(),
        }

        self.assertEqual(Comment.objects.count(), 0)
        self.resp_body = self.send_event(data)
        self.assertEqual(self.resp_body["success"], True)
        self.resp_body = self.resp_body["objs"]

        self.assertEqual(Comment.objects.count(), 1)
        c = Comment.objects.all()[0]
        obj_data = self.get_nested_obj(f"window.aurochs.data.frameworks['{obj.ox_id}']")

        self.assertEqual(obj_data["comments"][0]["body"], c.body)
        self.assertEqual(obj_data["comments"][0]["edited"], c.edited)
        self.assertEqual(obj_data["comments"][0]["id"], c.ox_id)
        self.assertEqual(
            obj_data["comments"][0]["user"],
            f"window.aurochs.data.users['{c.user.ox_id}']",
        )

        # Test editing
        data = {
            "event_type": "update_comment",
            "id": c.ox_id,
            "body": Factory.rand_text(),
        }

        self.resp_body = self.send_event(data)

        self.assertEqual(self.resp_body["success"], True)
        self.resp_body = self.resp_body["objs"]
        self.assertEqual(Comment.objects.count(), 1)
        obj_data = self.get_nested_obj(f"window.aurochs.data.frameworks['{obj.ox_id}']")

        self.assertEqual(obj_data["comments"][0]["body"], data["body"])
        self.assertEqual(obj_data["comments"][0]["edited"], True)
        self.assertEqual(obj_data["comments"][0]["id"], c.ox_id)
        self.assertEqual(
            obj_data["comments"][0]["user"],
            f"window.aurochs.data.users['{c.user.ox_id}']",
        )

        # Test deleting
        data = {
            "event_type": "delete_comment",
            "id": c.ox_id,
            "body": Factory.rand_text(),
        }

        self.resp_body = self.send_event(data)

        self.assertEqual(self.resp_body["success"], True)
        self.resp_body = self.resp_body["objs"]
        self.assertEqual(Comment.objects.count(), 0)
        obj_data = self.get_nested_obj(f"window.aurochs.data.frameworks['{obj.ox_id}']")

        self.assertEqual(obj_data["comments"], [])

    def test_add_edit_and_delete_on_report(self):
        obj = Factory.report(user=self.user)
        data = {
            "event_type": "add_comment",
            "object_type": "report",
            "id": obj.ox_id,
            "body": Factory.rand_text(),
        }

        self.assertEqual(Comment.objects.count(), 0)
        self.resp_body = self.send_event(data)
        self.assertEqual(self.resp_body["success"], True)
        self.resp_body = self.resp_body["objs"]

        self.assertEqual(Comment.objects.count(), 1)
        c = Comment.objects.all()[0]
        obj_data = self.get_nested_obj(f"window.aurochs.data.reports['{obj.ox_id}']")

        self.assertEqual(obj_data["comments"][0]["body"], c.body)
        self.assertEqual(obj_data["comments"][0]["edited"], c.edited)
        self.assertEqual(obj_data["comments"][0]["id"], c.ox_id)
        self.assertEqual(
            obj_data["comments"][0]["user"],
            f"window.aurochs.data.users['{c.user.ox_id}']",
        )
        # Test editing
        data = {
            "event_type": "update_comment",
            "id": c.ox_id,
            "body": Factory.rand_text(),
        }

        self.resp_body = self.send_event(data)

        self.assertEqual(self.resp_body["success"], True)
        self.resp_body = self.resp_body["objs"]
        self.assertEqual(Comment.objects.count(), 1)
        obj_data = self.get_nested_obj(f"window.aurochs.data.reports['{obj.ox_id}']")

        self.assertEqual(obj_data["comments"][0]["body"], data["body"])
        self.assertEqual(obj_data["comments"][0]["edited"], True)
        self.assertEqual(obj_data["comments"][0]["id"], c.ox_id)
        self.assertEqual(
            obj_data["comments"][0]["user"],
            f"window.aurochs.data.users['{c.user.ox_id}']",
        )

        # Test deleting
        data = {
            "event_type": "delete_comment",
            "id": c.ox_id,
            "body": Factory.rand_text(),
        }

        self.resp_body = self.send_event(data)

        self.assertEqual(self.resp_body["success"], True)
        self.resp_body = self.resp_body["objs"]
        self.assertEqual(Comment.objects.count(), 0)
        obj_data = self.get_nested_obj(f"window.aurochs.data.reports['{obj.ox_id}']")

        self.assertEqual(obj_data["comments"], [])

    def test_add_edit_and_delete_on_source(self):
        obj = Factory.source(user=self.user)
        data = {
            "event_type": "add_comment",
            "object_type": "source",
            "id": obj.ox_id,
            "body": Factory.rand_text(),
        }

        self.assertEqual(Comment.objects.count(), 0)
        self.resp_body = self.send_event(data)
        self.assertEqual(self.resp_body["success"], True)
        self.resp_body = self.resp_body["objs"]

        self.assertEqual(Comment.objects.count(), 1)
        c = Comment.objects.all()[0]
        obj_data = self.get_nested_obj(f"window.aurochs.data.sources['{obj.ox_id}']")

        self.assertEqual(obj_data["comments"][0]["body"], c.body)
        self.assertEqual(obj_data["comments"][0]["edited"], c.edited)
        self.assertEqual(obj_data["comments"][0]["id"], c.ox_id)
        self.assertEqual(
            obj_data["comments"][0]["user"],
            f"window.aurochs.data.users['{c.user.ox_id}']",
        )
        # Test editing
        data = {
            "event_type": "update_comment",
            "id": c.ox_id,
            "body": Factory.rand_text(),
        }

        self.resp_body = self.send_event(data)

        self.assertEqual(self.resp_body["success"], True)
        self.resp_body = self.resp_body["objs"]
        self.assertEqual(Comment.objects.count(), 1)
        obj_data = self.get_nested_obj(f"window.aurochs.data.sources['{obj.ox_id}']")

        self.assertEqual(obj_data["comments"][0]["body"], data["body"])
        self.assertEqual(obj_data["comments"][0]["edited"], True)
        self.assertEqual(obj_data["comments"][0]["id"], c.ox_id)
        self.assertEqual(
            obj_data["comments"][0]["user"],
            f"window.aurochs.data.users['{c.user.ox_id}']",
        )

        # Test deleting
        data = {
            "event_type": "delete_comment",
            "id": c.ox_id,
            "body": Factory.rand_text(),
        }

        self.resp_body = self.send_event(data)

        self.assertEqual(self.resp_body["success"], True)
        self.resp_body = self.resp_body["objs"]
        self.assertEqual(Comment.objects.count(), 0)
        obj_data = self.get_nested_obj(f"window.aurochs.data.sources['{obj.ox_id}']")

        self.assertEqual(obj_data["comments"], [])

    def test_editing_a_comment_that_is_not_yours_is_disallowed(self):
        obj = Factory.framework(user=self.user)
        data = {
            "event_type": "add_comment",
            "object_type": "framework",
            "id": obj.ox_id,
            "body": Factory.rand_text(),
        }

        self.assertEqual(Comment.objects.count(), 0)
        self.resp_body = self.send_event(data)
        self.assertEqual(self.resp_body["success"], True)
        self.resp_body = self.resp_body["objs"]

        u2, p2 = Factory.user()
        self.client.login(username=u2.username, password=p2)
        data2 = {
            "event_type": "add_comment",
            "object_type": "framework",
            "id": obj.ox_id,
            "body": Factory.rand_text(),
        }

        self.assertEqual(Comment.objects.count(), 1)
        self.resp_body = self.send_event(data2)
        self.assertEqual(self.resp_body["success"], False)
        self.assertEqual(Comment.objects.count(), 1)
        c = Comment.objects.all()[0]
        self.assertEqual(c.body, data["body"])

    def test_adding_a_comment_to_a_subscribed_framework_creates_inbox_items(self):
        u2, p2 = Factory.user()
        obj = Factory.framework(user=self.user)
        obj.set_permission(
            acting_user=self.user,
            user=u2,
            can_score=True,
            can_read=True,
            can_write=True,
            can_administer=False,
        )
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
        self.assertEqual(InboxItem.objects.count(), 0)

        # Create a comment as user 2
        self.client.login(username=u2.username, password=p2)
        data = {
            "event_type": "add_comment",
            "object_type": "framework",
            "id": obj.ox_id,
            "body": Factory.rand_text(),
        }

        self.assertEqual(Comment.objects.count(), 0)
        self.assertEqual(InboxItem.objects.count(), 0)
        self.resp_body = self.send_event(data)
        self.assertEqual(self.resp_body["success"], True)
        self.resp_body = self.resp_body["objs"]
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(InboxItem.objects.count(), 1)
        c = Comment.objects.all()[0]
        ii = InboxItem.objects.all()[0]
        self.assertEqual(ii.comment, c)
        self.assertEqual(ii.object_id, obj.id)
        self.assertEqual(ii.read, False)
        self.assertEqual(ii.done, False)

        # Ensure that it is listed for user 1 on their get.
        self.client.login(username=self.user.username, password=self.password)
        data = {
            "event_type": "get_my_user",
        }

        self.resp_body = self.send_event(data)
        self.assertEqual(self.resp_body["success"], True)
        self.resp_body = self.resp_body["objs"]
        user_data = self.get_nested_obj(
            f"window.aurochs.data.users['{self.user.ox_id}']"
        )
        self.assertEqual(
            user_data["inbox"],
            {
                "active": [f"{ii.ox_id}"],
                "done": [],
                "unread_count": 1,
            },
        )
        ii_data = self.get_nested_obj(f"window.aurochs.data.inboxitems['{ii.ox_id}']")
        self.assertEqual(ii_data["comment"]["body"], c.body)
        self.assertEqual(ii_data["comment"]["edited"], c.edited)
        self.assertEqual(ii_data["comment"]["id"], c.ox_id)
        self.assertEqual(
            ii_data["comment"]["user"], f"window.aurochs.data.users['{c.user.ox_id}']"
        )

    def test_adding_a_comment_to_a_subscribed_report_creates_inbox_items(self):
        u2, p2 = Factory.user()
        obj = Factory.report(user=self.user)
        obj.set_permission(
            acting_user=self.user,
            user=u2,
            can_score=True,
            can_read=True,
            can_write=True,
            can_administer=False,
        )
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

        # Create a comment as user 2
        self.client.login(username=u2.username, password=p2)
        data = {
            "event_type": "add_comment",
            "object_type": "report",
            "id": obj.ox_id,
            "body": Factory.rand_text(),
        }

        self.assertEqual(Comment.objects.count(), 0)
        self.resp_body = self.send_event(data)
        self.assertEqual(self.resp_body["success"], True)
        self.resp_body = self.resp_body["objs"]
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(InboxItem.objects.count(), 1)
        c = Comment.objects.all()[0]
        ii = InboxItem.objects.all()[0]
        self.assertEqual(ii.comment, c)
        self.assertEqual(ii.object_id, obj.id)

        # Ensure that it is listed for user 1 on their get.
        self.client.login(username=self.user.username, password=self.password)
        data = {
            "event_type": "get_report",
            "object_type": "report",
            "id": obj.ox_id,
        }

        self.resp_body = self.send_event(data)
        self.assertEqual(self.resp_body["success"], True)
        self.resp_body = self.resp_body["objs"]

        user_data = self.get_nested_obj(
            f"window.aurochs.data.users['{self.user.ox_id}']"
        )
        self.assertEqual(
            user_data["inbox"],
            {
                "active": [f"{ii.ox_id}"],
                "done": [],
                "unread_count": 1,
            },
        )
        ii_data = self.get_nested_obj(f"window.aurochs.data.inboxitems['{ii.ox_id}']")
        self.assertEqual(ii_data["comment"]["body"], c.body)
        self.assertEqual(ii_data["comment"]["edited"], c.edited)
        self.assertEqual(ii_data["comment"]["id"], c.ox_id)
        self.assertEqual(
            ii_data["comment"]["user"], f"window.aurochs.data.users['{c.user.ox_id}']"
        )

    def test_adding_a_comment_to_a_subscribed_source_creates_inbox_items(self):
        u2, p2 = Factory.user()
        obj = Factory.source(user=self.user)
        obj.set_permission(
            acting_user=self.user,
            user=u2,
            can_score=True,
            can_read=True,
            can_write=True,
            can_administer=False,
        )
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

        # Create a comment as user 2
        self.client.login(username=u2.username, password=p2)
        data = {
            "event_type": "add_comment",
            "object_type": "source",
            "id": obj.ox_id,
            "body": Factory.rand_text(),
        }

        self.assertEqual(Comment.objects.count(), 0)
        self.resp_body = self.send_event(data)
        self.assertEqual(self.resp_body["success"], True)
        self.resp_body = self.resp_body["objs"]
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(InboxItem.objects.count(), 1)
        c = Comment.objects.all()[0]
        ii = InboxItem.objects.all()[0]
        self.assertEqual(ii.comment, c)
        self.assertEqual(ii.object_id, obj.id)

        # Ensure that it is listed for user 1 on their get.
        self.client.login(username=self.user.username, password=self.password)
        data = {
            "event_type": "get_source",
            "object_type": "source",
            "id": obj.ox_id,
        }

        self.resp_body = self.send_event(data)
        self.assertEqual(self.resp_body["success"], True)
        self.resp_body = self.resp_body["objs"]
        user_data = self.get_nested_obj(
            f"window.aurochs.data.users['{self.user.ox_id}']"
        )
        self.assertEqual(
            user_data["inbox"],
            {
                "active": [f"{ii.ox_id}"],
                "done": [],
                "unread_count": 1,
            },
        )
        ii_data = self.get_nested_obj(f"window.aurochs.data.inboxitems['{ii.ox_id}']")
        self.assertEqual(ii_data["comment"]["body"], c.body)
        self.assertEqual(ii_data["comment"]["edited"], c.edited)
        self.assertEqual(ii_data["comment"]["id"], c.ox_id)
        self.assertEqual(
            ii_data["comment"]["user"], f"window.aurochs.data.users['{c.user.ox_id}']"
        )

    def test_adding_two_comments_by_users_puts_them_in_the_right_order(self):
        u2, p2 = Factory.user()
        obj = Factory.framework(user=self.user)
        obj.set_permission(
            acting_user=self.user,
            user=u2,
            can_score=True,
            can_read=True,
            can_write=True,
            can_administer=False,
        )
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

        # Create a comment as user 2
        self.client.login(username=u2.username, password=p2)
        data = {
            "event_type": "add_comment",
            "object_type": "framework",
            "id": obj.ox_id,
            "body": Factory.rand_text(),
        }

        self.assertEqual(Comment.objects.count(), 0)
        self.resp_body = self.send_event(data)
        self.assertEqual(self.resp_body["success"], True)
        self.resp_body = self.resp_body["objs"]
        d2 = data
        d2["body"] = Factory.rand_text()
        self.resp_body = self.send_event(data)
        self.assertEqual(self.resp_body["success"], True)
        self.resp_body = self.resp_body["objs"]

        self.assertEqual(Comment.objects.count(), 2)
        self.assertEqual(InboxItem.objects.count(), 1)
        c2 = Comment.objects.all()[1]
        ii = InboxItem.objects.all()[0]
        self.assertEqual(ii.comment, c2)
        self.assertEqual(ii.object_id, obj.id)

        # Ensure that it is listed for user 1 on their get.
        self.client.login(username=self.user.username, password=self.password)
        data = {
            "event_type": "get_framework",
            "object_type": "framework",
            "id": obj.ox_id,
        }

        self.resp_body = self.send_event(data)
        self.assertEqual(self.resp_body["success"], True)
        self.resp_body = self.resp_body["objs"]
        user_data = self.get_nested_obj(
            f"window.aurochs.data.users['{self.user.ox_id}']"
        )
        self.assertEqual(
            user_data["inbox"],
            {
                "active": [f"{ii.ox_id}"],
                "done": [],
                "unread_count": 1,
            },
        )
        ii_data = self.get_nested_obj(f"window.aurochs.data.inboxitems['{ii.ox_id}']")
        self.assertEqual(ii_data["comment"]["body"], c2.body)
        self.assertEqual(ii_data["comment"]["edited"], c2.edited)
        self.assertEqual(ii_data["comment"]["id"], c2.ox_id)
        self.assertEqual(
            ii_data["comment"]["user"], f"window.aurochs.data.users['{c2.user.ox_id}']"
        )

    def test_mark_inbox_item_done_moves_it_to_done(self):
        self.test_adding_a_comment_to_a_subscribed_report_creates_inbox_items()
        self.assertEqual(InboxItem.objects.count(), 1)
        ii = InboxItem.objects.all()[0]
        self.assertEqual(ii.done, False)
        data = {
            "event_type": "mark_inbox_item_done",
            "id": ii.ox_id,
        }

        self.resp_body = self.send_event(data)
        self.assertEqual(self.resp_body["success"], True)
        self.resp_body = self.resp_body["objs"]
        ii = InboxItem.objects.all()[0]
        self.assertEqual(ii.done, True)
        ii_data = self.get_nested_obj(f"window.aurochs.data.inboxitems['{ii.ox_id}']")
        self.assertEqual(ii_data["done"], True)

    def test_mark_inbox_item_active_moves_it_to_active(self):
        self.test_mark_inbox_item_done_moves_it_to_done()
        self.assertEqual(InboxItem.objects.count(), 1)
        ii = InboxItem.objects.all()[0]
        self.assertEqual(ii.done, True)
        data = {
            "event_type": "mark_inbox_item_active",
            "id": ii.ox_id,
        }

        self.resp_body = self.send_event(data)
        self.assertEqual(self.resp_body["success"], True)
        self.resp_body = self.resp_body["objs"]
        ii = InboxItem.objects.all()[0]
        self.assertEqual(ii.done, False)
        ii_data = self.get_nested_obj(f"window.aurochs.data.inboxitems['{ii.ox_id}']")
        self.assertEqual(ii_data["done"], False)

    def test_mark_inbox_item_read_moves_it_to_read(self):
        self.test_adding_a_comment_to_a_subscribed_report_creates_inbox_items()
        self.assertEqual(InboxItem.objects.count(), 1)
        ii = InboxItem.objects.all()[0]
        self.assertEqual(ii.read, False)
        data = {
            "event_type": "mark_inbox_item_read",
            "id": ii.ox_id,
        }

        self.resp_body = self.send_event(data)
        self.assertEqual(self.resp_body["success"], True)
        self.resp_body = self.resp_body["objs"]
        ii = InboxItem.objects.all()[0]
        self.assertEqual(ii.read, True)
        ii_data = self.get_nested_obj(f"window.aurochs.data.inboxitems['{ii.ox_id}']")
        self.assertEqual(ii_data["read"], True)

    def test_mark_inbox_item_unread_moves_it_to_unread(self):
        self.test_mark_inbox_item_read_moves_it_to_read()
        self.assertEqual(InboxItem.objects.count(), 1)
        ii = InboxItem.objects.all()[0]
        self.assertEqual(ii.read, True)
        data = {
            "event_type": "mark_inbox_item_unread",
            "id": ii.ox_id,
        }

        self.resp_body = self.send_event(data)
        self.assertEqual(self.resp_body["success"], True)
        self.resp_body = self.resp_body["objs"]
        ii = InboxItem.objects.all()[0]
        self.assertEqual(ii.read, False)
        ii_data = self.get_nested_obj(f"window.aurochs.data.inboxitems['{ii.ox_id}']")
        self.assertEqual(ii_data["read"], False)

    def test_two_user_self_comment_edge_case(self):
        # Set u2 with permissions to comment
        u2, p2 = Factory.user()
        obj = Factory.source(user=self.user)
        obj.set_permission(
            acting_user=self.user,
            user=u2,
            can_score=True,
            can_read=True,
            can_write=True,
            can_administer=False,
        )
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

        # User 2
        self.client.login(username=u2.username, password=p2)

        # Subscribe as user2

        data = {
            "event_type": "subscribe",
            "object_type": "source",
            "id": obj.ox_id,
        }
        self.resp_body = self.send_event(data)

        self.assertEqual(self.resp_body["success"], True)
        self.resp_body = self.resp_body["objs"]
        self.assertEqual(ObjectSubscription.objects.count(), 2)

        # Create a comment as user 2
        data = {
            "event_type": "add_comment",
            "object_type": "source",
            "id": obj.ox_id,
            "body": Factory.rand_text(),
        }

        self.assertEqual(Comment.objects.count(), 0)
        self.resp_body = self.send_event(data)
        self.assertEqual(self.resp_body["success"], True)
        self.resp_body = self.resp_body["objs"]

        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(InboxItem.objects.count(), 1)
        c1 = Comment.objects.all()[0]
        ii = InboxItem.objects.all()[0]
        self.assertEqual(ii.comment, c1)
        self.assertEqual(ii.object_id, obj.id)
        self.assertEqual(ii.user, self.user)

        # Ensure that it is not listed for user 2 on their get.
        data = {
            "event_type": "get_my_user",
        }
        self.resp_body = self.send_event(data)
        self.assertEqual(self.resp_body["success"], True)

        self.resp_body = self.resp_body["objs"]
        user_data = self.get_nested_obj(f"window.aurochs.data.users['{u2.ox_id}']")
        self.assertEqual(
            user_data["inbox"],
            {
                "active": [],
                "done": [],
                "unread_count": 0,
            },
        )

        # Ensure that it is listed for user 1 on their get.
        self.client.login(username=self.user.username, password=self.password)
        data = {
            "event_type": "get_my_user",
        }

        self.resp_body = self.send_event(data)
        self.assertEqual(self.resp_body["success"], True)
        self.resp_body = self.resp_body["objs"]
        user_data = self.get_nested_obj(
            f"window.aurochs.data.users['{self.user.ox_id}']"
        )
        self.assertEqual(
            user_data["inbox"],
            {
                "active": [f"{ii.ox_id}"],
                "done": [],
                "unread_count": 1,
            },
        )
        ii_data = self.get_nested_obj(f"window.aurochs.data.inboxitems['{ii.ox_id}']")
        self.assertEqual(ii_data["comment"]["body"], c1.body)
        self.assertEqual(ii_data["comment"]["edited"], c1.edited)
        self.assertEqual(ii_data["comment"]["id"], c1.ox_id)
        self.assertEqual(
            ii_data["comment"]["user"], f"window.aurochs.data.users['{c1.user.ox_id}']"
        )

        # Log back in as User 2
        self.client.login(username=u2.username, password=p2)
        # Get the homepage
        # self.client.get("/")

        # Post another a comment as user 2
        data = {
            "event_type": "add_comment",
            "object_type": "source",
            "id": obj.ox_id,
            "body": Factory.rand_text(),
        }

        self.assertEqual(Comment.objects.count(), 1)
        self.resp_body = self.send_event(data)
        self.assertEqual(self.resp_body["success"], True)
        self.resp_body = self.resp_body["objs"]

        self.assertEqual(Comment.objects.count(), 2)
        self.assertEqual(InboxItem.objects.count(), 1)
        c2 = Comment.objects.all()[1]
        ii = InboxItem.objects.all()[0]
        self.assertEqual(ii.comment, c2)
        self.assertEqual(ii.object_id, obj.id)
        self.assertEqual(ii.user, self.user)

        # Ensure that it is not listed for user 2 on their get.
        data = {
            "event_type": "get_my_user",
        }
        self.resp_body = self.send_event(data)
        self.assertEqual(self.resp_body["success"], True)
        self.resp_body = self.resp_body["objs"]
        user_data = self.get_nested_obj(f"window.aurochs.data.users['{u2.ox_id}']")
        self.assertEqual(
            user_data["inbox"],
            {
                "active": [],
                "done": [],
                "unread_count": 0,
            },
        )

        # Caching clears this, since it's the same response if there's nothing in the inbox.
        # user_data = self.get_nested_obj(
        #     f"window.aurochs.data.users['{u2.ox_id}']"
        # )
        #
        # self.assertEqual(
        #     user_data["inbox"],
        #     {
        #         "active": [],
        #         "done": [],
        #         "unread_count": 0,
        #     },
        # )
