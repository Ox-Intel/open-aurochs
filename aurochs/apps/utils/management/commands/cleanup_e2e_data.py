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
        from django.contrib.contenttypes.models import ContentType

        for o in Organization.objects.filter(name__startswith="e2eOrg - ").all():
            for orgrole in o.organizationrole_set.all():
                orgrole.user.delete()
            o.delete()
