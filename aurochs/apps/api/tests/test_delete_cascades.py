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
from sources.models import Source, SourceFeedback


class TestDeleteCascades(TestCase):
    def test_endpoint(self):
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(TeamMember.objects.count(), 0)
        self.assertEqual(Team.objects.count(), 0)

        t = Factory.team()
        u1, _ = Factory.user(organization=t.organization)
        u2, _ = Factory.user(organization=t.organization)
        t.add_user(u1)
        t.add_user(u2)

        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(TeamMember.objects.count(), 2)
        self.assertEqual(Team.objects.count(), 1)

        t.delete()
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(TeamMember.objects.count(), 0)
        self.assertEqual(Team.objects.count(), 0)
