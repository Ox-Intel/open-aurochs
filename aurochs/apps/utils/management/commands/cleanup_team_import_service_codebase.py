import json
from django.core.management.base import BaseCommand
from django.core.cache import cache


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        print(
            "This command is deprecated, as no Ox instances contain legacy data. If needed, roll back to code from November 25, 2022."
        )
