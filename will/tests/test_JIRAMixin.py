from mock import MagicMock, patch
import unittest
import requests

from will import settings
from will import utils
import json
import pep8

"""
class TestJIRAMixinPEP8(unittest.TestCase):
    def setUp(self):
        pass

    def test_PEP8Compliance(self):
        pep8style = pep8.StyleGuide()
        result = pep8style.check_files(['utils.py'])
        self.assertEqual(result.total_errors, 0,
                         'Found PEP8 complance issues/warnings.')
"""
class TestJIRAMixin(unittest.TestCase):
    def setUp(self):
        settings.JIRA_USERNAME = 'mlove'
        settings.JIRA_PASSWORD = '123'
        settings.JIRA_SERVER = 'test.com'


    def test_ClientSetup(self):

        from will.mixins import JIRAMixin

        self.assertTrue(JIRAMixin.client)

    @patch('will.utils._RESTClient.request')
    def test_get_project_multi(self, mock_call):

        from will.mixins import JIRAMixin

        data = [{'id':123, 'key':'ABC', 'name':'test1'},
                {'id':456, 'key':'DEF', 'name':'test2'},
                {'id':789, 'key':'GH9', 'name':'test3'}]
        mock_call.return_value=json.dumps(data)
        r = JIRAMixin.get_project(proj_key=None)
        mock_call.assert_called_with('GET',
                                     '/rest/api/2/project/',
                                     cb=JIRAMixin.client.strip_data)

        self.assertEqual(mock_call.return_value, r)

    @patch('will.utils._RESTClient.request')
    def test_get_project_one(self, mock_call):

        from will.mixins import JIRAMixin
        data = [{'id':123, 'key':'ABC', 'name':'test1'}]
        mock_call.return_value=json.dumps(data)
        r = JIRAMixin.get_project(proj_key='ABC')
        mock_call.assert_called_with('GET',
                                     '/rest/api/2/project/ABC',
                                     cb=JIRAMixin.client.strip_data)

        self.assertEqual(mock_call.return_value, r)

    @patch('will.mixins.JIRAMixin.get_project')
    def test_get_project_keys(self, mock_call):

        from will.mixins import JIRAMixin

        data = [{'id':123, 'key':'ABC', 'name':'test1'},
                {'id':456, 'key':'DEF', 'name':'test2'},
                {'id':789, 'key':'GH9', 'name':'test3'}]

        mock_call.return_value=data

        r = JIRAMixin.get_project_keys()
        mock_call.assert_called_with(proj_key=None)
        self.assertEqual(['ABC','DEF','GH9'], list(r))

    @patch('will.utils._RESTClient.request')
    def test_create_project(self, mock_call):

        from will.mixins import JIRAMixin

        data = [{'id':123, 'key':'ABC', 'name':'test1'}]

        mock_call.return_value=json.dumps(data)
        r = JIRAMixin.create_project('Test 1', 'ABC','user1')

        calldata = {"key": "ABC",
                    "name": "Test 1",
                    "projectTypeKey": "software",
                    "projectTemplateKey": "com.pyxis.greenhopper.jira:gh-scrum-template",
                    "lead": "user1"}

        mock_call.assert_called_with('POST',
                                     '/rest/api/2/project/',
                                     cb=JIRAMixin.client.strip_data,
                                     data=calldata)

        self.assertEqual(mock_call.return_value, r)

    @patch('will.utils._RESTClient.request')
    def test_get_project_roles(self, mock_call):

        from will.mixins import JIRAMixin
        data = [{'id': '10001', 'name': 'Admin'},
                {'id': '10002', 'name': 'Developer'},
                {'id': '10003', 'name': 'Lead'}]

        proj_key = 'ABC123'
        mock_call.return_value=json.dumps(data)

        r = JIRAMixin.get_project_roles(proj_key)

        mock_call.assert_called_with('GET',
                                     '/rest/api/2/project/ABC123/role/',
                                     cb=JIRAMixin.client.strip_data)
        self.assertEqual(mock_call.return_value,r)


    @patch('will.utils._RESTClient.request')
    def test_assign_project_role(self, mock_call):

        from will.mixins import JIRAMixin

        proj_key = 'ABC123'

        r = JIRAMixin.assign_project_role('user1', proj_key, '10002')

        mock_call.assert_called_with('POST',
                                     '/rest/api/2/project/ABC123/role/10002',
                                     cb=JIRAMixin.client.strip_data,
                                     data={'user':['user1']})
