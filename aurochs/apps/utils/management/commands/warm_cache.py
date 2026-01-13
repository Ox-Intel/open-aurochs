import sys
import json
from django.core.management.base import BaseCommand
from django.core.cache import cache


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        from archives.models import HistoricalEvent
        from collaboration.models import InboxItem
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
        from stacks.models import Stack

        # For all objects that can have a _to_json, call it and cache it.
        # def warm_model(model):
        #     print(f"\nWarming {model.__name__}s...")
        #     if hasattr(model, "raw_objects"):
        #         for obj in model.raw_objects.all():
        #             sys.stdout.write(".")
        #             sys.stdout.flush()
        #     else:
        #         for obj in model.objects.all():
        #             sys.stdout.write(".")
        #             sys.stdout.flush()

        # warm_model(Organization)
        # warm_model(Team)
        # warm_model(User)
        # warm_model(SourceFeedback)
        # warm_model(Source)
        # warm_model(Criteria)
        # warm_model(Scorecard)
        # warm_model(ScorecardScore)
        # warm_model(Report)
        # warm_model(Framework)

        # Change to warming per-user.
        # print("Warming for each user...")
        # for user in User.objects.all():

        #     # Data for aurochs
        #     frameworks = (
        #         Framework.authorized_objects.authorize(user=user)
        #         .findable.all()
        #         .order_by("pk")
        #     )
        #     reports = (
        #         Report.authorized_objects.authorize(user=user)
        #         .findable.all()
        #         .order_by("pk")
        #     )
        #     sources = (
        #         Source.authorized_objects.authorize(user=user)
        #         .findable.all()
        #         .order_by("pk")
        #     )
        #     stacks = (
        #         Stack.authorized_objects.authorize(user=user)
        #         .findable.all()
        #         .order_by("pk")
        #     )
        #     inboxitems = InboxItem.objects.filter(user=user).all()

        #     js_objects = []
        #     js_objects.append(user)
        #     js_objects.extend(frameworks)
        #     js_objects.extend(reports)
        #     js_objects.extend(sources)
        #     js_objects.extend(stacks)
        #     js_objects.extend(inboxitems)
        #     js_objects.extend(user.teams)
        #     js_objects.extend(user.organizations)

        #     sys.stdout.write(".")
        #     sys.stdout.flush()

        print("done.")
