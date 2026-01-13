from decimal import Decimal
import mock
import unittest
from django.test import TestCase
from utils.factory import Factory
from frameworks.models import Framework
from reports.models import Report, Scorecard, ScorecardScore


class TestOutcomeScoreScorecard(TestCase):
    def test_outcome_score_calculations(self):
        f = Factory.framework()

        r1 = Factory.report(feedback_score=95)
        Factory.scorecard(report=r1, framework=f)

        r2 = Factory.report(feedback_score=100)
        Factory.scorecard(report=r2, framework=f)

        r3 = Factory.report(feedback_score=100)
        Factory.scorecard(report=r3, framework=f)

        r4 = Factory.report(feedback_score=None)
        Factory.scorecard(report=r4, framework=f)

        f = Framework.objects.get(ox_id=f.ox_id)
        self.assertEqual(f.average_feedback_score, Decimal("98.33333"))

        r4.feedback_score = 0
        r4.save()

        f = Framework.objects.get(ox_id=f.ox_id)
        self.assertEqual(f.average_feedback_score, Decimal("73.75"))

    def test_outcome_score_null(self):
        f = Factory.framework()

        r = Factory.report(feedback_score=None)
        Factory.scorecard(report=r, framework=f)
        r2 = Factory.report(feedback_score=None)
        Factory.scorecard(report=r2, framework=f)
        r3 = Factory.report(feedback_score=None)
        Factory.scorecard(report=r3, framework=f)
        r4 = Factory.report(feedback_score=None)
        Factory.scorecard(report=r4, framework=f)

        f = Framework.objects.get(ox_id=f.ox_id)
        self.assertEqual(f.average_feedback_score, None)
