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
    User,
    Organization,
    OrganizationRole,
    GenericPermission,
)
from reports.models import Report, Scorecard, ScorecardScore
from sources.models import Source, SourceFeedback


class TestCreateOrganization(EventTestCase):
    def test_organization_admin_can_delete_organization(self):
        o = Factory.organization()
        o.add_user(self.user, can_manage=True)

        self.assertEqual(Organization.objects.all().count(), 1)
        self.assertEqual(OrganizationRole.objects.all().count(), 1)
        data = {"event_type": "delete_organization", "id": o.ox_id}

        self.resp_body = self.send_event(data)

        self.assertEqual(self.resp_body["success"], True)
        self.resp_body = self.resp_body["objs"]
        self.assertEqual(Organization.objects.all().count(), 0)
        self.assertEqual(OrganizationRole.objects.all().count(), 0)

    def test_other_users_cannot_delete_organization(self):
        o = Factory.organization()

        self.assertEqual(Organization.objects.all().count(), 1)
        self.assertEqual(OrganizationRole.objects.all().count(), 0)
        data = {"event_type": "delete_organization", "id": o.ox_id}

        self.resp_body = self.send_event(data)

        self.assertEqual(self.resp_body["success"], False)
        self.assertEqual(Organization.objects.all().count(), 1)

    def test_organization_with_sole_content_cannot_be_deleted(self):
        o = Factory.organization()
        o.add_user(self.user, can_manage=True)

        u2, p2 = Factory.user()
        f = Factory.framework(organization=o, user=u2)
        f.remove_permission(acting_user=self.user, user=u2)

        self.assertEqual(GenericPermission.objects.all().count(), 1)

        data = {"event_type": "delete_organization", "id": o.ox_id}

        self.resp_body = self.send_event(data)

        self.assertEqual(self.resp_body["success"], False)
        self.assertEqual(Organization.objects.all().count(), 1)
        self.assertEqual(GenericPermission.objects.all().count(), 1)
