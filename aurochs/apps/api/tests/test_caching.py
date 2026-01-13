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


class TestCaching(EventTestCase):
    def test_adding_two_comments_by_users_returns_them_in_the_frameworks(self):
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
        self.client2 = Client()
        self.client2.login(username=u2.username, password=p2)
        data = {
            "event_type": "add_comment",
            "object_type": "framework",
            "id": obj.ox_id,
            "body": Factory.rand_text(),
        }

        self.assertEqual(Comment.objects.count(), 0)
        self.resp_body = self.send_event(data, client=self.client2)
        self.assertEqual(self.resp_body["success"], True)
        d2 = data
        d2["body"] = Factory.rand_text()
        self.resp_body = self.send_event(data, client=self.client2)
        self.assertEqual(self.resp_body["success"], True)

        self.assertEqual(Comment.objects.count(), 2)
        self.assertEqual(InboxItem.objects.count(), 1)
        c1 = Comment.objects.all()[0]
        c2 = Comment.objects.all()[1]
        ii = InboxItem.objects.all()[0]
        self.assertEqual(ii.comment, c2)
        self.assertEqual(ii.object_id, obj.id)

        # Ensure that it is listed for user 1 on their get.
        data = {
            "event_type": "get_framework",
            "id": obj.ox_id,
        }

        self.resp_body = self.send_event(data)
        self.assertEqual(self.resp_body["success"], True)
        obj_data = self.get_nested_obj(f"window.aurochs.data.frameworks['{obj.ox_id}']")

        self.assertEqual(obj_data["comments"][0]["body"], c1.body)
        self.assertEqual(obj_data["comments"][0]["edited"], c1.edited)
        self.assertEqual(obj_data["comments"][0]["id"], c1.ox_id)
        self.assertEqual(
            obj_data["comments"][0]["user"],
            f"window.aurochs.data.users['{c1.user.ox_id}']",
        )
        self.assertEqual(obj_data["comments"][1]["body"], c2.body)
        self.assertEqual(obj_data["comments"][1]["edited"], c2.edited)
        self.assertEqual(obj_data["comments"][1]["id"], c2.ox_id)
        self.assertEqual(
            obj_data["comments"][1]["user"],
            f"window.aurochs.data.users['{c2.user.ox_id}']",
        )

        # Ensure that it is listed for user 1 on their get.
        self.client.login(username=u2.username, password=p2)
        data = {
            "event_type": "get_my_user",
        }

        self.resp_body = self.send_event(data)
        self.assertEqual(self.resp_body["success"], True)

        obj_data = self.get_nested_obj(f"window.aurochs.data.frameworks['{obj.ox_id}']")

        self.assertEqual(obj_data["comments"][0]["body"], c1.body)
        self.assertEqual(obj_data["comments"][0]["edited"], c1.edited)
        self.assertEqual(obj_data["comments"][0]["id"], c1.ox_id)
        self.assertEqual(
            obj_data["comments"][0]["user"],
            f"window.aurochs.data.users['{c1.user.ox_id}']",
        )
        self.assertEqual(obj_data["comments"][1]["body"], c2.body)
        self.assertEqual(obj_data["comments"][1]["edited"], c2.edited)
        self.assertEqual(obj_data["comments"][1]["id"], c2.ox_id)
        self.assertEqual(
            obj_data["comments"][1]["user"],
            f"window.aurochs.data.users['{c2.user.ox_id}']",
        )
