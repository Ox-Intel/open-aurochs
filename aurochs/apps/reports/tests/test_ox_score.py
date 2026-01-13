from decimal import Decimal
import mock
import unittest
from django.test import TestCase
from utils.factory import Factory
from reports.models import Report, Scorecard, ScorecardScore


class TestOxScoreScorecard(TestCase):
    def test_ox_score_calculations(self):
        f = Factory.framework()
        c1 = Factory.criteria(framework=f, weight=1)
        c2 = Factory.criteria(framework=f, weight=5)

        sc1 = Factory.scorecard(framework=f)
        Factory.scorecard_score(scorecard=sc1, score=8, criteria=c1)
        Factory.scorecard_score(scorecard=sc1, score=2, criteria=c2)
        sc1 = Scorecard.objects.get(ox_id=sc1.ox_id)
        self.assertEqual(sc1.ox_score, 30)

        f = Factory.framework()
        c1 = Factory.criteria(framework=f, weight=10)
        c2 = Factory.criteria(framework=f, weight=3)

        sc2 = Factory.scorecard(framework=f)
        Factory.scorecard_score(scorecard=sc2, score=3, criteria=c1)
        Factory.scorecard_score(scorecard=sc2, score=8, criteria=c2)
        sc2 = Scorecard.objects.get(ox_id=sc2.ox_id)
        self.assertEqual(sc2.ox_score, Decimal("42"))

    def test_ox_score_null(self):
        f = Factory.framework()
        Factory.criteria(framework=f, weight=1)
        Factory.criteria(framework=f, weight=5)

        sc1 = Factory.scorecard(framework=f)
        self.assertEqual(sc1.ox_score, None)

    def test_ox_score_with_skipped(self):
        f = Factory.framework()
        c1 = Factory.criteria(framework=f, weight=1)
        c2 = Factory.criteria(framework=f, weight=5)
        r1 = Factory.report()
        r2 = Factory.report()

        sc1 = Factory.scorecard(framework=f, report=r1)
        Factory.scorecard_score(scorecard=sc1, score=8, criteria=c1)
        Factory.scorecard_score(scorecard=sc1, score=2, criteria=c2)
        sc1 = Scorecard.objects.get(ox_id=sc1.ox_id)
        self.assertEqual(sc1.ox_score, 30)
        self.assertEqual(r1.ox_score, 30)
        self.assertEqual(sc1.has_skipped, False)
        self.assertEqual(r1.has_skipped, False)

        f = Factory.framework()
        c1 = Factory.criteria(framework=f, weight=10)
        c2 = Factory.criteria(framework=f, weight=3)

        sc2 = Factory.scorecard(framework=f, report=r2)
        Factory.scorecard_score(scorecard=sc2, score=None, criteria=c1)
        Factory.scorecard_score(scorecard=sc2, score=8, criteria=c2)
        sc2 = Scorecard.objects.get(ox_id=sc2.ox_id)
        self.assertEqual(sc2.ox_score, Decimal("18"))
        self.assertEqual(r2.ox_score, Decimal("18"))

        self.assertEqual(sc2.has_skipped, True)
        self.assertEqual(r2.has_skipped, True)

        sc3 = Factory.scorecard(framework=f, report=r2)
        Factory.scorecard_score(scorecard=sc3, score=3, criteria=c1)
        Factory.scorecard_score(scorecard=sc3, score=None, criteria=c2)
        sc3 = Scorecard.objects.get(ox_id=sc3.ox_id)
        r2 = Report.raw_objects.get(ox_id=r2.ox_id)
        self.assertEqual(sc3.ox_score, Decimal("23"))
        self.assertEqual(r2.ox_score, Decimal("42"))

        self.assertEqual(sc3.has_skipped, True)
        self.assertEqual(r2.has_skipped, False)
