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


class TestDeleteScorecard(EventTestCase):
    def test_endpoint(self):
        self.assertEqual(Scorecard.objects.count(), 0)
        f = Factory.framework(user=self.user)
        Factory.criteria(framework=f, user=self.user)
        Factory.criteria(framework=f, user=self.user)
        r = Factory.report(framework=f, user=self.user)
        sc = Factory.scorecard(framework=f, report=r, user=self.user)
        Factory.scorecard_score(scorecard=sc, score=Factory.rand_int(start=1, end=10))

        self.assertEqual(Scorecard.objects.count(), 1)
        self.assertEqual(ScorecardScore.objects.count(), 1)
        self.assertEqual(Framework.objects.count(), 2)
        self.assertEqual(Report.objects.count(), 1)
        self.assertEqual(Criteria.objects.count(), 3)

        data = {
            "event_type": "delete_scorecard",
            "id": sc.ox_id,
        }

        # sent_time = self.now()
        self.resp_body = self.send_event(data)

        self.assertEqual(self.resp_body["success"], True)
        self.resp_body = self.resp_body["objs"]
        self.assertEqual(Framework.objects.count(), 2)
        self.assertEqual(Report.objects.count(), 1)
        self.assertEqual(Criteria.objects.count(), 3)
        self.assertEqual(Scorecard.objects.count(), 0)
        self.assertEqual(ScorecardScore.objects.count(), 0)
