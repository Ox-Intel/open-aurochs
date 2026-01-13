from datetime import datetime
from decimal import Decimal
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


class TestCreateScorecard(EventTestCase):
    def test_endpoint(self):
        f = Factory.framework(user=self.user)
        c1 = Factory.criteria(framework=f, user=self.user)
        c2 = Factory.criteria(framework=f, user=self.user)
        r = Factory.report(framework=f, user=self.user)

        self.assertEqual(Scorecard.objects.count(), 0)
        self.assertEqual(ScorecardScore.objects.count(), 0)
        data = {
            "event_type": "create_scorecard",
            "report_id": r.ox_id,
            "framework_id": f.ox_id,
            "scores": [
                {
                    "criteria_id": c1.ox_id,
                    "comment": Factory.rand_str(),
                    "score": Factory.rand_int(start=1, end=10),
                    "gpt_scored_last": False,
                },
                {
                    "criteria_id": c2.ox_id,
                    "comment": Factory.rand_str(),
                    "score": Factory.rand_int(start=1, end=10),
                    "gpt_scored_last": False,
                },
            ],
        }

        sent_time = self.now()
        self.resp_body = self.send_event(data)

        self.assertEqual(self.resp_body["success"], True)
        self.resp_body = self.resp_body["objs"]
        self.assertEqual(Scorecard.objects.count(), 1)
        self.assertEqual(ScorecardScore.objects.count(), 2)
        scs1, scs2 = [scs for scs in ScorecardScore.objects.order_by("-created_at")]

        obj = Scorecard.objects.all()[0]
        self.assertEqual(obj.framework, f)
        self.assertEqual(obj.report, r)

        obj_data = self.get_nested_obj(f"window.aurochs.data.reports['{r.ox_id}']")
        obj_data = obj_data["scorecards"][0]

        # Source Data
        user_str = f"window.aurochs.data.users['{self.user.ox_id}']"

        self.assertEqual(obj_data["__type"], "scorecard")
        # "created_at": "2022-04-12T19:18:30.437Z",
        self.assertBasicallyEqualTimes(
            datetime.fromtimestamp(int(obj_data["created_at_ms"]) / 1000), sent_time
        )
        # "created_at_ms": 1649791110437.731,
        # "created_by": user,
        self.assertEqual(obj_data["scorer"], user_str)
        # "deleted": false,

        # "deleted_at": null,

        # "id": 1,
        self.assertEqual(obj_data["id"], obj.ox_id)
        # "modified_at": "2022-04-12T19:18:30.443Z",
        # "modified_at_ms": 1649791110443.849,
        # "modified_by": null,

        # "name": "R\\u2764\\ud83c\\udf81\\ud83d\\udc8cF\\u2642\\ud83c\\udfa7\\ud83c\\udf31Dl",
        self.assertEqual(
            obj_data["framework"], f"window.aurochs.data.frameworks['{f.ox_id}']"
        )
        # self.assertEqual(
        #     obj_data["report"], f"window.aurochs.data.reports['{r.ox_id}']"
        # )

        self.assertEqual(obj_data["scores"][0]["id"], scs2.ox_id)
        self.assertEqual(obj_data["scores"][0]["score"], str(scs2.score))
        self.assertEqual(obj_data["scores"][0]["scorer"], user_str)
        self.assertEqual(obj_data["scores"][0]["comment"], scs2.comment)
        self.assertEqual(
            obj_data["scores"][0]["criteria"],
            f"window.aurochs.data.criterias['{c1.ox_id}']",
        )

        self.assertEqual(obj_data["scores"][1]["id"], scs1.ox_id)
        self.assertEqual(obj_data["scores"][1]["score"], str(scs1.score))
        self.assertEqual(obj_data["scores"][1]["scorer"], user_str)
        self.assertEqual(obj_data["scores"][1]["comment"], scs1.comment)
        self.assertEqual(
            obj_data["scores"][1]["criteria"],
            f"window.aurochs.data.criterias['{c2.ox_id}']",
        )
