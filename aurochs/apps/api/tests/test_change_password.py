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


class TestUpdateSource(EventTestCase):
    def test_endpoint(self):
        self.assertTrue(self.user.check_password(self.password))
        data = {
            "event_type": "change_password",
            "new_password": Factory.rand_str(),
        }

        self.resp_body = self.send_event(data)

        self.assertEqual(self.resp_body["success"], True)
        # Update from cached object.
        self.user = User.objects.get(pk=self.user.pk)

        self.assertFalse(self.user.check_password(self.password))
        self.assertTrue(self.user.check_password(data["new_password"]))
