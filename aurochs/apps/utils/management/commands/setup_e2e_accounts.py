import json
from django.core.management.base import BaseCommand
from django.core.cache import cache


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        from archives.models import HistoricalEvent
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
        from utils.factory import Factory

        ox_org, _ = Organization.objects.get_or_create(
            name="ox-intel",
            description="Ox admin organization",
        )

        cust_org, _ = Organization.objects.get_or_create(
            name="customer-one",
            description="Customer one test organization",
        )
        cust_org2, _ = Organization.objects.get_or_create(
            name="customer-two",
            description="Customer two test organization",
        )
        cust_org3, _ = Organization.objects.get_or_create(
            name="customer-three",
            description="Customer three test organization",
        )
        cust_org4, _ = Organization.objects.get_or_create(
            name="customer-four",
            description="Customer four test organization",
        )
        test_super, test_super_pass = Factory.user(
            username="test-super",
            first_name="e2eTest",
            last_name="Super",
            password="0x1ntelEnter",
            email="test-super@oxintel.org",
            is_ox_staff=True,
            is_superuser=True,
        )
        admin, admin_pass = Factory.user(
            username="ox-admin",
            first_name="Admin",
            last_name="Ox-intel",
            password="Ox1ntelEnter",
            email="info@oxintel.org",
            organization=ox_org,
            is_ox_staff=True,
            is_superuser=True,
        )
        cust_super, cust_super_pass = Factory.user(
            username="cust-super",
            first_name="Super",
            last_name="Customer",
            organization=cust_org,
            password="0x1ntelEnter",
            email="cust-super@oxintel.org",
        )
        cust_org.add_user(cust_super, can_view=True, can_manage=True)
        cust_admin, cust_admin_pass = Factory.user(
            username="cust-admin",
            first_name="Admin",
            last_name="Customer",
            organization=cust_org,
            password="0x1ntelEnter",
            email="cust-admin@oxintel.org",
            is_ox_staff=True,
            is_superuser=True,
        )
        cust_org.add_user(cust_admin, can_view=True, can_manage=True)
        cust_user, cust_user_pass = Factory.user(
            username="cust-user",
            first_name="User",
            last_name="Customer",
            organization=cust_org,
            password="0x1ntelEnter",
            email="cust-user@oxintel.org",
        )
        # Organization 2 users:
        cust_super2, cust_super2_pass = Factory.user(
            username="cust-super2",
            first_name="Super",
            last_name="Customer 2",
            organization=cust_org2,
            password="0x1ntelEnter",
            email="cust-super2@oxintel.org",
        )
        cust_org2.add_user(cust_super2, can_view=True, can_manage=True)
        cust_admin2, cust_admin2_pass = Factory.user(
            username="cust-admin2",
            first_name="Admin",
            last_name="Customer 2",
            organization=cust_org2,
            password="0x1ntelEnter",
            email="cust-admin2@oxintel.org",
            is_ox_staff=True,
            is_superuser=True,
        )
        cust_org2.add_user(cust_admin2, can_view=True, can_manage=True)
        cust_user2, cust_user2_pass = Factory.user(
            username="cust-user2",
            first_name="User",
            last_name="Customer 2",
            organization=cust_org2,
            password="0x1ntelEnter",
            email="cust-user2@oxintel.org",
        )
        # Organization 3 users:
        cust_super3, cust_super3_pass = Factory.user(
            username="cust-super3",
            first_name="Super",
            last_name="Customer 3",
            organization=cust_org3,
            password="0x1ntelEnter",
            email="cust-super3@oxintel.org",
        )
        cust_org3.add_user(cust_super3, can_view=True, can_manage=True)
        cust_admin3, cust_admin3_pass = Factory.user(
            username="cust-admin3",
            first_name="Admin",
            last_name="Customer 3",
            organization=cust_org3,
            password="0x1ntelEnter",
            email="cust-admin3@oxintel.org",
            is_ox_staff=True,
            is_superuser=True,
        )
        cust_org3.add_user(cust_admin3, can_view=True, can_manage=True)
        cust_user3, cust_user3_pass = Factory.user(
            username="cust-user3",
            first_name="User",
            last_name="Customer 3",
            organization=cust_org3,
            password="0x1ntelEnter",
            email="cust-user3@oxintel.org",
        )
        # Organization 4 users:
        cust_super4, cust_super4_pass = Factory.user(
            username="cust-super4",
            first_name="Super",
            last_name="Customer 4",
            organization=cust_org4,
            password="0x1ntelEnter",
            email="cust-super4@oxintel.org",
        )
        cust_org4.add_user(cust_super4, can_view=True, can_manage=True)
        cust_admin4, cust_admin4_pass = Factory.user(
            username="cust-admin4",
            first_name="Admin",
            last_name="Customer 4",
            organization=cust_org4,
            password="0x1ntelEnter",
            email="cust-admin4@oxintel.org",
            is_ox_staff=True,
            is_superuser=True,
        )
        cust_org4.add_user(cust_admin3, can_view=True, can_manage=True)
        cust_user4, cust_user4_pass = Factory.user(
            username="cust-user4",
            first_name="User",
            last_name="Customer 4",
            organization=cust_org4,
            password="0x1ntelEnter",
            email="cust-user4@oxintel.org",
        )
