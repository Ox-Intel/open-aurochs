import datetime
import time

from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = "Resets the dev database"

    def add_arguments(self, parser):
        parser.add_argument("--confirm", type=bool)

    def handle(self, *args, **options):
        if hasattr(settings, "IS_LIVE") and settings.IS_LIVE:
            print("In production (IS_LIVE=True).  Refusing to run.")
            return

        if "confirm" not in options:
            print("Missing --confirm")
            return

        pass
