import json
import mock
import unittest
from django.test import TestCase
from django.test import Client
from django.utils import timezone
from utils.factory import Factory
from django.core.cache import cache


class EventTestCase(TestCase):
    def setUp(self, *args, **kwargs):
        cache.clear()
        self.maxDiff = 999999999
        self.client = Client()
        self.user, self.password = Factory.user()
        self.login()
        super(EventTestCase, self).setUp(*args, **kwargs)

    def tearDown(self):
        self.login()

    def login(self):
        self.client.login(username=self.user.username, password=self.password)

    def send_event(self, data, client=None):
        if not client:
            client = self.client
        resp = client.post(
            "/event/",
            json.dumps(data),
            content_type="application/json",
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.assertEqual(resp.status_code, 200)
        # print(resp.json())
        return json.loads(resp.json())

    def now(self):
        return timezone.now()

    def assertBasicallyEqualTimes(self, t1, t2):  # noqa
        # self.assertEqual(t1.tzinfo, t2.tzinfo)
        if not t1.tzinfo:
            t1 = t1.replace(tzinfo=timezone.utc)
        if not t2.tzinfo:
            t2 = t2.replace(tzinfo=timezone.utc)
        diff = abs((t2 - t1).total_seconds())
        self.assertTrue(diff < 6)

    def _replace_window_aurochs(self, js_str):
        replacements = js_str.split("window.aurochs.data.")
        out_str = ""
        first = True
        for r in replacements:
            if first:
                out_str += r
                first = False
            else:
                trailing_brace = r.find("']")
                line = (
                    '"window.aurochs.data.'
                    + r[:trailing_brace]
                    + "']\""
                    + r[trailing_brace + 2 :]
                )
                out_str += line
        return out_str

    def get_nested_obj(self, obj_str):
        obj_list = self.resp_body
        if "objs" in self.resp_body:
            obj_list = self.resp_body["objs"]
        for i in obj_list:
            if obj_str in i:
                if i[obj_str][-1] == ";":
                    return json.loads(self._replace_window_aurochs(i[obj_str][:-1]))
                return json.loads(self._replace_window_aurochs(i[obj_str]))

    def assertInObjList(self, key, val):
        obj_list = self.resp_body
        if "objs" in self.resp_body:
            obj_list = self.resp_body["objs"]
        for i in obj_list:
            if key in i:
                return self.assertEqual(i[key], val)
        return self.assertEqual(False, val)
