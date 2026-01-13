import mock
import unittest
from django.test import TestCase
from utils.factory import Factory
from frameworks.models import Criteria, Framework
from reports.models import Report, Scorecard, ScorecardScore


class TestOxScoreReport(TestCase):
    def test_ox_score_calculations(self):
        self.user, self.password = Factory.user()
        f = Factory.framework(user=self.user)
        c1 = Factory.criteria(framework=f, weight=1)
        c2 = Factory.criteria(framework=f, weight=5)
        r = Factory.report(framework=f, user=self.user)

        sc1 = Factory.scorecard(framework=f, report=r, scorer=self.user)
        Factory.scorecard_score(scorecard=sc1, score=8, criteria=c1)
        Factory.scorecard_score(scorecard=sc1, score=2, criteria=c2)
        r = Report.authorized_objects.authorize(user=self.user).findable.get(
            ox_id=r.ox_id
        )
        sc1 = Scorecard.objects.get(ox_id=sc1.ox_id)
        self.assertEqual(sc1.ox_score, 30)
        self.assertEqual(r.ox_score, 30)

        sc2 = Factory.scorecard(framework=f, report=r, scorer=self.user)
        Factory.scorecard_score(scorecard=sc2, score=1, criteria=c1)
        Factory.scorecard_score(scorecard=sc2, score=7, criteria=c2)
        r = Report.raw_objects.get(ox_id=r.ox_id)
        sc2 = Scorecard.objects.get(ox_id=sc2.ox_id)
        self.assertEqual(sc2.ox_score, 60)
        self.assertEqual(r.ox_score, 45)

    def test_ox_score_null(self):
        r = Factory.report()
        self.assertEqual(r.ox_score, None)

        sc = Factory.scorecard()
        self.assertEqual(sc.ox_score, None)
