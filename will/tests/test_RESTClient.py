from mock import MagicMock, patch
import unittest

from will.utils import RESTClient, _BasicRESTClient
import requests
import json
class TestRESTClientFactory(unittest.TestCase):
    def setUp(self):
        pass
    def test_BasicClient_lower(self):
        self.assertIsInstance(RESTClient.client('basic','test.com','mlove','123'),_BasicRESTClient)
        self.assertIsInstance(RESTClient.client('bAsiC','test.com','mlove','123'),_BasicRESTClient)
        self.assertIsInstance(RESTClient.client('BASIC','test.com','mlove','123'),_BasicRESTClient)

class Test_BasicRESTClient(unittest.TestCase):
    def setUp(self):
        self.client = RESTClient.client('basic','test.com', 'mlove', '123')

    def test_Base_URL(self):
        self.assertTrue(self.client.base)
    def test__uri_join(self):
        self.assertEqual(self.client._uri_join('/api/v2'),'http://test.com/api/v2')
    def test_SessionConstruction(self):
        self.assertIsInstance(self.client._sess, requests.Session)
    """@patch('requests.request')
    def test_POST_ok(self, mock_post):
        target_response = {'data':[{'key':'value'}]}
        mock_post.return_value = MagicMock(spec=requests.Response,
                                           status_code=200,
                                           response=json.dumps(target_response))
        r = self.client.request('post','/api/v2')
        self.assertEqual(r,r)
"""

