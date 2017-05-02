from mock import MagicMock, patch
import unittest

from will import settings
import json
import pep8

class TestJIRAMixinPEP8(unittest.TestCase):
    def setUp(self):
        pass

    def test_PEP8Compliance(self):
        pep8style = pep8.StyleGuide()
        result = pep8style.check_files(['utils.py'])
        self.assertEqual(result.total_errors, 0,
                         'Found PEP8 complance issues/warnings.')

class TestJIRAMixin(unittest.TestCase):
    def setUp(self):
        settings.JIRA_USERNAME = 'mlove'
        settings.JIRA_PASSWORD = '123'
        settings.JIRA_SERVER = 'test.com'

    def test_ClientSetup(self):
        from will.mixins import JIRAMixin
        self.client = JIRAMixin()
        self.assertTrue(self.client)


