import mock
import unittest
from django.test import TestCase
from utils.factory import Factory
from frameworks.models import Criteria, Framework
from organizations.models import (
    Organization,
    Team,
    TeamMember,
    User,
    OrganizationRole,
    GenericPermission,
)
from reports.models import Report, Scorecard, ScorecardScore
from sources.models import Source, SourceFeedback


class TestSoftDelete(TestCase):
    def test_soft_delete_deletes_from_queryset(self):
        o1 = Factory.organization()
        u1, p1 = Factory.user(organization=o1)

        f = Factory.framework(user=u1)
        Factory.criteria(framework=f, user=u1)
        Factory.criteria(framework=f, user=u1)
        r = Factory.report(framework=f, user=u1)
        Factory.scorecard(report=r, framework=f, scorer=u1, user=u1)

        self.assertEqual(Framework.objects_with_deleted.count(), 1)
        self.assertEqual(Criteria.objects_with_deleted.count(), 2)
        self.assertEqual(Report.objects_with_deleted.count(), 1)
        self.assertEqual(Scorecard.objects_with_deleted.count(), 1)

        f.delete()

        self.assertEqual(Framework.objects.count(), 0)
        self.assertEqual(Criteria.objects.count(), 0)
        self.assertEqual(Report.objects.count(), 1)
        self.assertEqual(Scorecard.objects.count(), 0)

    def test_soft_delete_cascades(self):
        o1 = Factory.organization()
        u1, p1 = Factory.user(organization=o1)

        f = Factory.framework(user=u1)
        c1 = Factory.criteria(framework=f, user=u1)
        c2 = Factory.criteria(framework=f, user=u1)
        r = Factory.report(framework=f, user=u1)
        sc = Factory.scorecard(report=r, framework=f, scorer=u1, user=u1)

        self.assertEqual(f.deleted, False)
        self.assertEqual(c1.deleted, False)
        self.assertEqual(c2.deleted, False)
        self.assertEqual(r.deleted, False)
        self.assertEqual(sc.deleted, False)

        f.delete()
        f = Framework.objects_with_deleted.get(ox_id=f.ox_id)
        c1 = Criteria.objects_with_deleted.get(ox_id=c1.ox_id)
        c2 = Criteria.objects_with_deleted.get(ox_id=c2.ox_id)
        r = Report.objects_with_deleted.get(ox_id=r.ox_id)
        sc = Scorecard.objects_with_deleted.get(ox_id=sc.ox_id)

        self.assertEqual(f.deleted, True)
        self.assertEqual(c1.deleted, True)
        self.assertEqual(c2.deleted, True)
        self.assertEqual(r.deleted, False)
        self.assertEqual(sc.deleted, True)
