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

        superuser, created = User.objects.get_or_create(
            username="admin",
        )

        superuser.is_superuser = True
        superuser.is_ox_staff = True
        superuser.save()

        superuser, created = User.objects.get_or_create(
            username="org-admin",
        )

        superuser.is_superuser = True
        superuser.is_ox_staff = True
        superuser.save()
