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


class TestTaggingFrameworks(EventTestCase):
    def test_basic_setting_framework(self):
        o = Factory.organization()
        self.user, password = Factory.user(organization=o)
        self.client.login(username=self.user.username, password=password)
        f = Factory.framework(organization=o, user=self.user)
        data = {
            "event_type": "update_framework",
            "id": f.ox_id,
            "name": Factory.rand_str(),
            "tags": [
                {
                    "name": Factory.rand_str(),
                },
                {
                    "name": Factory.rand_str(),
                },
            ],
        }

        self.resp_body = self.send_event(data)

        self.assertEqual(self.resp_body["success"], True)
        self.resp_body = self.resp_body["objs"]
        self.assertEqual(Framework.objects.all().count(), 1)
        f = Framework.objects.all()[0]
        self.assertEqual(TaggedObject.objects.all().count(), 2)
        self.assertEqual(Tag.objects.all().count(), 2)
        t0 = Tag.objects.all()[0]
        self.assertEqual(t0.name, data["tags"][0]["name"])
        t1 = Tag.objects.all()[1]
        self.assertEqual(t1.name, data["tags"][1]["name"])

        obj_data = self.get_nested_obj(f"window.aurochs.data.frameworks['{f.ox_id}']")

        # Framework Data
        # "window.aurochs.data.frameworks['1']": '{"__type": "framework",
        self.assertEqual(obj_data["__type"], "framework")
        self.assertEqual(
            obj_data["tags"],
            [
                f"window.aurochs.data.tags['{t0.ox_id}']",
                f"window.aurochs.data.tags['{t1.ox_id}']",
            ],
        )
        self.assertEqual(
            obj_data["search_text"],
            f"framework:{f.ox_id}|name:{f.name}|tag:{t0.name}|tag:{t1.name}|",
        )

    def test_basic_setting_one_tag_framework(self):
        o = Factory.organization()
        self.user, password = Factory.user(organization=o)
        self.client.login(username=self.user.username, password=password)
        f = Factory.framework(organization=o, user=self.user)
        data = {
            "event_type": "update_framework",
            "id": f.ox_id,
            "name": Factory.rand_str(),
            "tags": [
                {
                    "name": Factory.rand_str(),
                },
            ],
        }

        self.resp_body = self.send_event(data)

        self.assertEqual(self.resp_body["success"], True)
        self.resp_body = self.resp_body["objs"]
        self.assertEqual(Framework.objects.all().count(), 1)
        f = Framework.objects.all()[0]
        self.assertEqual(TaggedObject.objects.all().count(), 1)
        self.assertEqual(Tag.objects.all().count(), 1)
        t0 = Tag.objects.all()[0]
        self.assertEqual(t0.name, data["tags"][0]["name"])

        obj_data = self.get_nested_obj(f"window.aurochs.data.frameworks['{f.ox_id}']")

        # Framework Data
        # "window.aurochs.data.frameworks['1']": '{"__type": "framework",
        self.assertEqual(obj_data["__type"], "framework")
        self.assertEqual(
            obj_data["tags"],
            [
                f"window.aurochs.data.tags['{t0.ox_id}']",
            ],
        )
        self.assertEqual(
            obj_data["search_text"], f"framework:{f.ox_id}|name:{f.name}|tag:{t0.name}|"
        )

    def test_basic_setting_report(self):
        o = Factory.organization()
        self.user, password = Factory.user(organization=o)
        self.client.login(username=self.user.username, password=password)
        r = Factory.report(organization=o, user=self.user)
        data = {
            "event_type": "update_report",
            "id": r.ox_id,
            "name": Factory.rand_str(),
            "tags": [
                {
                    "name": Factory.rand_str(),
                },
                {
                    "name": Factory.rand_str(),
                },
            ],
        }

        self.resp_body = self.send_event(data)

        self.assertEqual(self.resp_body["success"], True)
        self.resp_body = self.resp_body["objs"]
        self.assertEqual(Report.objects.all().count(), 1)
        r = Report.objects.all()[0]
        self.assertEqual(TaggedObject.objects.all().count(), 2)
        self.assertEqual(Tag.objects.all().count(), 2)
        t0 = Tag.objects.all()[0]
        self.assertEqual(t0.name, data["tags"][0]["name"])
        t1 = Tag.objects.all()[1]
        self.assertEqual(t1.name, data["tags"][1]["name"])

        obj_data = self.get_nested_obj(f"window.aurochs.data.reports['{r.ox_id}']")

        # report Data
        # "window.aurochs.data.reports['1']": '{"__type": "report",
        self.assertEqual(obj_data["__type"], "report")
        self.assertEqual(
            obj_data["tags"],
            [
                f"window.aurochs.data.tags['{t0.ox_id}']",
                f"window.aurochs.data.tags['{t1.ox_id}']",
            ],
        )
        self.assertEqual(
            obj_data["search_text"],
            f"report:{r.ox_id}|name:{r.name}|tag:{t0.name}|tag:{t1.name}|",
        )

    def test_basic_setting_source(self):
        o = Factory.organization()
        self.user, password = Factory.user(organization=o)
        self.client.login(username=self.user.username, password=password)
        s = Factory.source(organization=o, user=self.user)
        data = {
            "event_type": "update_source",
            "id": s.ox_id,
            "name": Factory.rand_str(),
            "tags": [
                {
                    "name": Factory.rand_str(),
                },
                {
                    "name": Factory.rand_str(),
                },
            ],
        }

        self.resp_body = self.send_event(data)

        self.assertEqual(self.resp_body["success"], True)
        self.resp_body = self.resp_body["objs"]
        self.assertEqual(Source.objects.all().count(), 1)
        s = Source.objects.all()[0]
        self.assertEqual(TaggedObject.objects.all().count(), 2)
        self.assertEqual(Tag.objects.all().count(), 2)
        t0 = Tag.objects.all()[0]
        self.assertEqual(t0.name, data["tags"][0]["name"])
        t1 = Tag.objects.all()[1]
        self.assertEqual(t1.name, data["tags"][1]["name"])

        obj_data = self.get_nested_obj(f"window.aurochs.data.sources['{s.ox_id}']")

        # source Data
        # "window.aurochs.data.sources['1']": '{"__type": "source",
        self.assertEqual(obj_data["__type"], "source")
        self.assertEqual(
            obj_data["tags"],
            [
                f"window.aurochs.data.tags['{t0.ox_id}']",
                f"window.aurochs.data.tags['{t1.ox_id}']",
            ],
        )
        self.assertEqual(
            obj_data["search_text"],
            f"source:{s.ox_id}|name:{s.name}|tag:{t0.name}|tag:{t1.name}|",
        )

    def test_basic_setting_stack(self):
        o = Factory.organization()
        self.user, password = Factory.user(organization=o)
        self.client.login(username=self.user.username, password=password)
        s = Factory.stack(organization=o, user=self.user)
        data = {
            "event_type": "update_stack",
            "id": s.ox_id,
            "name": Factory.rand_str(),
            "tags": [
                {
                    "name": Factory.rand_str(),
                },
                {
                    "name": Factory.rand_str(),
                },
            ],
        }

        self.resp_body = self.send_event(data)

        self.assertEqual(self.resp_body["success"], True)
        self.resp_body = self.resp_body["objs"]
        self.assertEqual(Stack.objects.all().count(), 1)
        s = Stack.objects.all()[0]
        self.assertEqual(TaggedObject.objects.all().count(), 2)
        self.assertEqual(Tag.objects.all().count(), 2)
        t0 = Tag.objects.all()[0]
        self.assertEqual(t0.name, data["tags"][0]["name"])
        t1 = Tag.objects.all()[1]
        self.assertEqual(t1.name, data["tags"][1]["name"])

        obj_data = self.get_nested_obj(f"window.aurochs.data.stacks['{s.ox_id}']")

        # stack Data
        # "window.aurochs.data.stacks['1']": '{"__type": "stack",
        self.assertEqual(obj_data["__type"], "stack")
        self.assertEqual(
            obj_data["tags"],
            [
                f"window.aurochs.data.tags['{t0.ox_id}']",
                f"window.aurochs.data.tags['{t1.ox_id}']",
            ],
        )
        self.assertEqual(
            obj_data["search_text"],
            f"stack:{s.ox_id}|name:{s.name}|tag:{t0.name}|tag:{t1.name}|",
        )

    def test_tags_across_several_users_work_correctly(self):
        o = Factory.organization()
        o2 = Factory.organization()
        self.user1, password = Factory.user(organization=o)
        self.user2, password2 = Factory.user(organization=o2)
        self.client.login(username=self.user1.username, password=password)
        f = Factory.framework(organization=o, user=self.user1)
        f.set_permission(
            acting_user=self.user1,
            user=self.user2,
            can_score=True,
            can_read=True,
            can_write=True,
            can_administer=True,
        )

        data1 = {
            "event_type": "update_framework",
            "id": f.ox_id,
            "name": Factory.rand_str(),
            "tags": [
                {
                    "name": "Tag A",
                },
                {
                    "name": "Tag B",
                },
            ],
        }

        self.resp_body = self.send_event(data1)

        self.assertEqual(self.resp_body["success"], True)
        self.resp_body = self.resp_body["objs"]
        self.assertEqual(Framework.objects.all().count(), 1)
        f = Framework.objects.all()[0]
        self.assertEqual(TaggedObject.objects.all().count(), 2)
        self.assertEqual(Tag.objects.all().count(), 2)
        self.assertEqual(Tag.objects.all()[0].name, data1["tags"][0]["name"])
        self.assertEqual(Tag.objects.all()[1].name, data1["tags"][1]["name"])

        self.client.login(username=self.user2.username, password=password2)
        data2 = {
            "event_type": "update_framework",
            "id": f.ox_id,
            "name": Factory.rand_str(),
            "tags": [
                {
                    "name": "Tag B",
                },
                {
                    "name": "Tag C",
                },
            ],
        }

        self.resp_body = self.send_event(data2)

        self.assertEqual(self.resp_body["success"], True)
        self.resp_body = self.resp_body["objs"]
        self.assertEqual(Framework.objects.all().count(), 1)
        f = Framework.objects.all()[0]
        self.assertEqual(TaggedObject.objects.all().count(), 4)
        self.assertEqual(Tag.objects.all().count(), 4)
        self.assertEqual(Tag.objects.all()[0].name, "Tag A")
        self.assertEqual(Tag.objects.all()[0].organization, o)
        self.assertEqual(Tag.objects.all()[1].name, "Tag B")
        self.assertEqual(Tag.objects.all()[1].organization, o)
        self.assertEqual(Tag.objects.all()[2].name, "Tag B")
        self.assertEqual(Tag.objects.all()[2].organization, None)
        self.assertEqual(Tag.objects.all()[2].user, self.user2)
        self.assertEqual(Tag.objects.all()[3].name, "Tag C")
        self.assertEqual(Tag.objects.all()[3].organization, None)
        self.assertEqual(Tag.objects.all()[3].user, self.user2)

        # Deleting works, too.
        data2 = {
            "event_type": "update_framework",
            "id": f.ox_id,
            "name": Factory.rand_str(),
            "tags": [
                {
                    "name": Tag.objects.all()[2].name,
                },
            ],
        }

        self.resp_body = self.send_event(data2)
        self.assertEqual(TaggedObject.objects.all().count(), 3)
        self.assertEqual(Tag.objects.all().count(), 3)

    def test_deleting_tags_works(self):
        o = Factory.organization()
        self.user, password = Factory.user(organization=o)
        self.client.login(username=self.user.username, password=password)
        f = Factory.framework(organization=o, user=self.user)
        data = {
            "event_type": "update_framework",
            "id": f.ox_id,
            "name": Factory.rand_str(),
            "tags": [
                {
                    "name": Factory.rand_str(),
                },
                {
                    "name": Factory.rand_str(),
                },
            ],
        }

        self.resp_body = self.send_event(data)

        self.assertEqual(self.resp_body["success"], True)
        self.resp_body = self.resp_body["objs"]
        self.assertEqual(Framework.objects.all().count(), 1)
        f = Framework.objects.all()[0]
        self.assertEqual(TaggedObject.objects.all().count(), 2)
        self.assertEqual(Tag.objects.all().count(), 2)
        t0 = Tag.objects.all()[0]
        self.assertEqual(t0.name, data["tags"][0]["name"])
        t1 = Tag.objects.all()[1]
        self.assertEqual(t1.name, data["tags"][1]["name"])

        obj_data = self.get_nested_obj(f"window.aurochs.data.frameworks['{f.ox_id}']")

        # Framework Data
        # "window.aurochs.data.frameworks['1']": '{"__type": "framework",
        self.assertEqual(obj_data["__type"], "framework")
        self.assertEqual(
            obj_data["tags"],
            [
                f"window.aurochs.data.tags['{t0.ox_id}']",
                f"window.aurochs.data.tags['{t1.ox_id}']",
            ],
        )

        data = {
            "event_type": "update_framework",
            "id": f.ox_id,
            "name": Factory.rand_str(),
            "tags": [],
        }

        self.resp_body = self.send_event(data)
        self.assertEqual(self.resp_body["success"], True)

        self.assertEqual(TaggedObject.objects.all().count(), 0)
        self.assertEqual(Tag.objects.all().count(), 0)

    def test_tags_for_user_with_no_org_works_correctly(self):
        f = Factory.framework(user=self.user)
        data = {
            "event_type": "update_framework",
            "id": f.ox_id,
            "name": Factory.rand_str(),
            "tags": [
                {
                    "name": Factory.rand_str(),
                },
                {
                    "name": Factory.rand_str(),
                },
            ],
        }

        self.resp_body = self.send_event(data)

        self.assertEqual(self.resp_body["success"], True)
        self.resp_body = self.resp_body["objs"]
        self.assertEqual(Framework.objects.all().count(), 1)
        f = Framework.objects.all()[0]
        self.assertEqual(TaggedObject.objects.all().count(), 2)
        self.assertEqual(Tag.objects.all().count(), 2)
        t0 = Tag.objects.all()[0]
        self.assertEqual(t0.name, data["tags"][0]["name"])
        self.assertEqual(t0.user, self.user)
        t1 = Tag.objects.all()[1]
        self.assertEqual(t1.name, data["tags"][1]["name"])
        self.assertEqual(t1.user, self.user)

        obj_data = self.get_nested_obj(f"window.aurochs.data.frameworks['{f.ox_id}']")

        # Framework Data
        # "window.aurochs.data.frameworks['1']": '{"__type": "framework",
        self.assertEqual(obj_data["__type"], "framework")
        self.assertEqual(
            obj_data["tags"],
            [
                f"window.aurochs.data.tags['{t0.ox_id}']",
                f"window.aurochs.data.tags['{t1.ox_id}']",
            ],
        )

    def test_tags_for_nightmare_sometimes_org_user(self):
        f = Factory.framework(user=self.user)
        data = {
            "event_type": "update_framework",
            "id": f.ox_id,
            "name": Factory.rand_str(),
            "tags": [
                {
                    "name": Factory.rand_str(),
                },
                {
                    "name": Factory.rand_str(),
                },
            ],
        }

        self.resp_body = self.send_event(data)

        self.assertEqual(self.resp_body["success"], True)
        self.resp_body = self.resp_body["objs"]

        self.assertEqual(TaggedObject.objects.all().count(), 2)
        self.assertEqual(Tag.objects.all().count(), 2)

        o = Factory.organization()
        o.add_user(self.user)

        f.set_permission(
            acting_user=self.user,
            organization=o,
            can_score=True,
            can_read=True,
            can_write=True,
            can_administer=True,
        )

        data = {
            "event_type": "update_framework",
            "id": f.ox_id,
            "name": Factory.rand_str(),
            "tags": [
                {
                    "name": Factory.rand_str(),
                },
            ],
        }

        self.resp_body = self.send_event(data)
        self.assertEqual(TaggedObject.objects.all().count(), 1)
        self.assertEqual(Tag.objects.all().count(), 1)
        self.assertEqual(Tag.objects.all()[0].user, None)
        self.assertEqual(Tag.objects.all()[0].organization, o)

        o.remove_user(self.user)
        data = {
            "event_type": "update_framework",
            "id": f.ox_id,
            "name": Factory.rand_str(),
            "tags": [
                {
                    "name": Factory.rand_str(),
                },
            ],
        }

        self.resp_body = self.send_event(data)
        self.assertEqual(TaggedObject.objects.all().count(), 2)
        self.assertEqual(Tag.objects.all().count(), 2)
        self.assertEqual(Tag.objects.all()[0].user, None)
        self.assertEqual(Tag.objects.all()[0].organization, o)
        self.assertEqual(Tag.objects.all()[1].user, self.user)
        self.assertEqual(Tag.objects.all()[1].organization, None)

    def test_tags_adds_to_all_orgs(self):
        f = Factory.framework(user=self.user)
        o1 = Factory.organization()
        o1.add_user(self.user)
        o2 = Factory.organization()
        o2.add_user(self.user)
        f.set_permission(
            organization=o1,
            can_score=True,
            can_read=True,
            can_write=True,
            acting_user=self.user,
        )
        f.set_permission(
            organization=o2,
            can_score=True,
            can_read=True,
            can_write=True,
            acting_user=self.user,
        )
        data = {
            "event_type": "update_framework",
            "id": f.ox_id,
            "name": Factory.rand_str(),
            "tags": [
                {
                    "name": Factory.rand_str(),
                },
                {
                    "name": Factory.rand_str(),
                },
            ],
        }

        self.resp_body = self.send_event(data)

        self.assertEqual(self.resp_body["success"], True)
        self.resp_body = self.resp_body["objs"]

        self.assertEqual(TaggedObject.objects.all().count(), 4)
        self.assertEqual(Tag.objects.all().count(), 4)

    def test_users_from_the_same_org_share_tags_and_dont_delete(self):
        u2, p2 = Factory.user()
        o1 = Factory.organization()
        f = Factory.framework(organization=o1)
        o1.add_user(self.user)
        o1.add_user(u2)

        data = {
            "event_type": "update_framework",
            "id": f.ox_id,
            "name": Factory.rand_str(),
            "tags": [
                {
                    "name": Factory.rand_str(),
                },
                {
                    "name": Factory.rand_str(),
                },
            ],
        }

        self.resp_body = self.send_event(data)

        self.assertEqual(self.resp_body["success"], True)
        self.assertEqual(TaggedObject.objects.all().count(), 2)
        self.assertEqual(Tag.objects.all().count(), 2)

        self.client.login(username=u2.username, password=p2)
        self.resp_body = self.send_event(data)
        self.assertEqual(self.resp_body["success"], True)
        self.assertEqual(TaggedObject.objects.all().count(), 2)
        self.assertEqual(Tag.objects.all().count(), 2)

    def test_deleting_a_framework_with_the_last_tag_deletes_that_tag(self):
        o1 = Factory.organization()
        f = Factory.framework(organization=o1)
        o1.add_user(self.user)

        data = {
            "event_type": "update_framework",
            "id": f.ox_id,
            "name": Factory.rand_str(),
            "tags": [
                {
                    "name": Factory.rand_str(),
                },
            ],
        }

        self.resp_body = self.send_event(data)

        self.assertEqual(self.resp_body["success"], True)
        self.assertEqual(TaggedObject.objects.all().count(), 1)
        self.assertEqual(Tag.objects.all().count(), 1)
        data = {
            "event_type": "delete_framework",
            "id": f.ox_id,
        }

        self.resp_body = self.send_event(data)

        self.assertEqual(self.resp_body["success"], True)
        self.assertEqual(TaggedObject.objects.all().count(), 0)
        self.assertEqual(Tag.objects.all().count(), 0)

    def test_deleting_a_report_with_the_last_tag_deletes_that_tag(self):
        o1 = Factory.organization()
        f = Factory.report(organization=o1)
        o1.add_user(self.user)

        data = {
            "event_type": "update_report",
            "id": f.ox_id,
            "name": Factory.rand_str(),
            "tags": [
                {
                    "name": Factory.rand_str(),
                },
            ],
        }

        self.resp_body = self.send_event(data)

        self.assertEqual(self.resp_body["success"], True)
        self.assertEqual(TaggedObject.objects.all().count(), 1)
        self.assertEqual(Tag.objects.all().count(), 1)
        data = {
            "event_type": "delete_report",
            "id": f.ox_id,
        }

        self.resp_body = self.send_event(data)

        self.assertEqual(self.resp_body["success"], True)
        self.assertEqual(TaggedObject.objects.all().count(), 0)
        self.assertEqual(Tag.objects.all().count(), 0)

    def test_deleting_a_source_with_the_last_tag_deletes_that_tag(self):
        o1 = Factory.organization()
        f = Factory.source(organization=o1)
        o1.add_user(self.user)

        data = {
            "event_type": "update_source",
            "id": f.ox_id,
            "name": Factory.rand_str(),
            "tags": [
                {
                    "name": Factory.rand_str(),
                },
            ],
        }

        self.resp_body = self.send_event(data)

        self.assertEqual(self.resp_body["success"], True)
        self.assertEqual(TaggedObject.objects.all().count(), 1)
        self.assertEqual(Tag.objects.all().count(), 1)
        data = {
            "event_type": "delete_source",
            "id": f.ox_id,
        }

        self.resp_body = self.send_event(data)

        self.assertEqual(self.resp_body["success"], True)
        self.assertEqual(TaggedObject.objects.all().count(), 0)
        self.assertEqual(Tag.objects.all().count(), 0)
