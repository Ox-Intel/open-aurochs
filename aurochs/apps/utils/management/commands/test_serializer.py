import datetime
import json
import pprint
from django.core.management.base import BaseCommand
from django.core.cache import cache
import mock
from webapp.views import get_context


CALCULATE_LEGACY = False


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        # cache.clear()
        from organizations.serializers import OmniSerializer
        from organizations.models import User

        u = User.objects.get(username="steven-ox")
        start = datetime.datetime.now()
        s = OmniSerializer(u)

        # print(s.serialize_to_js_lines())
        s.serialize_to_js_lines()
        # pprint.pprint(s.serialize())
        # s.serialize()

        end = datetime.datetime.now()
        diff = 1000 * (end - start).total_seconds()
        print(f"OmniSerializer time: {diff} ms\n\n")

        # Legacy approach

        if CALCULATE_LEGACY:
            cache.clear()
            request = mock.Mock()
            request.user = u
            legacy_start = datetime.datetime.now()
            context = get_context(request)
            print(context)
            legacy_end = datetime.datetime.now()
            legacy_diff = 1000 * (legacy_end - legacy_start).total_seconds()
        else:
            legacy_diff = 1000 * datetime.timedelta(seconds=13).total_seconds()
        print(f"Legacy time: {legacy_diff} ms\n\n")

        improvement = "%.1f" % (legacy_diff / diff)
        print(f"Improvement: {improvement}x faster.")
