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


class TestReportSources(EventTestCase):
    def test_add_source_endpoint(self):
        r = Factory.report(user=self.user)
        s = Factory.source(user=self.user)
        self.assertEqual(len(r.authorized_sources), 0)
        data = {
            "event_type": "add_source_to_report",
            "report_id": r.ox_id,
            "source_id": s.ox_id,
        }

        self.resp_body = self.send_event(data)

        self.assertEqual(self.resp_body["success"], True)
        self.resp_body = self.resp_body["objs"]
        self.assertEqual(len(r.authorized_sources), 1)

        self.assertEqual(Report.objects.all().count(), 1)
        r = Report.objects.all()[0]

        report_data = self.get_nested_obj(f"window.aurochs.data.reports['{r.ox_id}']")
        source_data = self.get_nested_obj(f"window.aurochs.data.sources['{s.ox_id}']")

        # Report Data
        # "window.aurochs.data.reports['1']": '{"__type": "report",
        self.assertEqual(report_data["__type"], "report")
        self.assertEqual(source_data["__type"], "source")

        self.assertEqual(
            report_data["sources"], [f"window.aurochs.data.sources['{s.ox_id}']"]
        )

    def test_remove_source_endpoint(self):
        r = Factory.report(user=self.user)
        s = Factory.source(user=self.user)
        r.sources.add(s)
        r.save()
        self.assertEqual(len(r.authorized_sources), 1)
        data = {
            "event_type": "remove_source_from_report",
            "report_id": r.ox_id,
            "source_id": s.ox_id,
        }

        self.resp_body = self.send_event(data)

        self.assertEqual(self.resp_body["success"], True)
        self.resp_body = self.resp_body["objs"]
        self.assertEqual(len(r.authorized_sources), 0)

        self.assertEqual(Report.objects.all().count(), 1)
        r = Report.objects.all()[0]

        report_data = self.get_nested_obj(f"window.aurochs.data.reports['{r.ox_id}']")
        # Report Data
        # "window.aurochs.data.reports['1']": '{"__type": "report",
        self.assertEqual(report_data["__type"], "report")

        self.assertEqual(report_data["sources"], [])
