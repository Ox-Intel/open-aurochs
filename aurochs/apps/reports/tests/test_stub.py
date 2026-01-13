import mock
import unittest
from django.test import TestCase


class TestStub(TestCase):
    def test_runs(self):
        self.assertEqual(2, 1 + 1)
