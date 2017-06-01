from mock import MagicMock, patch
import unittest
import requests

from will import settings

settings.JIRA_USERNAME = 'mlove'
settings.JIRA_PASSWORD = '123'
settings.JIRA_SERVER = 'test.com'

from will import utils
import json
import pep8


from will.mixins import JIRAMixin
class TestJIRAMixinPEP8(unittest.TestCase):
    def setUp(self):
        pass

    def test_PEP8Compliance(self):
        pep8style = pep8.StyleGuide()
        result = pep8style.check_files(['mixins/jira.py'])
        self.assertEqual(result.total_errors, 0,
                         'Found PEP8 complance issues/warnings.')

class TestJIRAMixin(unittest.TestCase, JIRAMixin):
    def setUp(self):
        pass

    def test_ClientSetup(self):


        self.assertTrue(self.jclient)

    @patch('will.utils._RESTClient.request')
    def test_get_project_multi(self, mock_call):

        data = [{'id':123, 'key':'ABC', 'name':'test1'},
                {'id':456, 'key':'DEF', 'name':'test2'},
                {'id':789, 'key':'GH9', 'name':'test3'}]
        mock_call.return_value=json.dumps(data)
        r = self.get_jira_project(proj_key=None)
        mock_call.assert_called_with('GET',
                                     '/rest/api/2/project/',
                                     cb=self.jclient.strip_data)

        self.assertEqual(mock_call.return_value, r)

    @patch('will.utils._RESTClient.request')
    def test_get_project_one(self, mock_call):

        data = [{'id':123, 'key':'ABC', 'name':'test1'}]
        mock_call.return_value=json.dumps(data)
        r = self.get_jira_project(proj_key='ABC')
        mock_call.assert_called_with('GET',
                                     '/rest/api/2/project/ABC',
                                     cb=self.jclient.strip_data)

        self.assertEqual(mock_call.return_value, r)

    @patch('will.mixins.JIRAMixin.get_jira_project')
    def test_get_project_keys(self, mock_call):

        data = [{'id':123, 'key':'ABC', 'name':'test1'},
                {'id':456, 'key':'DEF', 'name':'test2'},
                {'id':789, 'key':'GH9', 'name':'test3'}]

        mock_call.return_value=data

        r = self.get_jira_project_keys()
        mock_call.assert_called_with(proj_key=None)
        self.assertEqual(['ABC','DEF','GH9'], list(r))

    @patch('will.utils._RESTClient.request')
    def test_create_project(self, mock_call):

        data = [{'id':123, 'key':'ABC', 'name':'test1'}]

        mock_call.return_value=json.dumps(data)
        r = self.create_jira_project('Test 1', 'ABC','user1')

        calldata = {"key": "ABC",
                    "name": "Test 1",
                    "projectTypeKey": "software",
                    "projectTemplateKey": "com.pyxis.greenhopper.jira:gh-scrum-template",
                    "lead": "user1"}

        mock_call.assert_called_with('POST',
                                     '/rest/api/2/project/',
                                     cb=self.jclient.strip_data,
                                     data=calldata)

        self.assertEqual(mock_call.return_value, r)

    @patch('will.utils._RESTClient.request')
    def test_get_project_roles(self, mock_call):

        data = [{'id': '10001', 'name': 'Admin'},
                {'id': '10002', 'name': 'Developer'},
                {'id': '10003', 'name': 'Lead'}]

        proj_key = 'ABC123'
        mock_call.return_value=json.dumps(data)

        r = self.get_jira_project_roles(proj_key)

        mock_call.assert_called_with('GET',
                                     '/rest/api/2/project/ABC123/role/',
                                     cb=self.jclient.strip_data)
        self.assertEqual(mock_call.return_value,r)


    @patch('will.utils._RESTClient.request')
    def test_assign_project_role(self, mock_call):

        proj_key = 'ABC123'

        r = self.assign_jira_project_role('user1', proj_key, '10002')

        mock_call.assert_called_with('POST',
                                     '/rest/api/2/project/ABC123/role/10002',
                                     cb=self.jclient.strip_data,
                                     data={'user':['user1']})
