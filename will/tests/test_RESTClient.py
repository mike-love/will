from mock import MagicMock, patch
import unittest

from will.utils import RESTClient, BasicRESTClient
import requests
import json
import pep8
"""
class TestRESTClientPEP8(unittest.TestCase):
    def setUp(self):
        pass
    def test_PEP8Compliance(self):
        pep8style = pep8.StyleGuide()
        result = pep8style.check_files(['utils.py'])
        self.assertEqual(result.total_errors, 0,
                         'Found PEP8 complance issues/warnings.')
"""
"""
# TODO: Remove Test with class
class TestRESTClientFactory(unittest.TestCase):
    def setUp(self):
        pass
    def test_BasicClient_lower(self):
        self.assertIsInstance(RESTClient.client('basic','test.com','mlove','123'),_BasicRESTClient)
        self.assertIsInstance(RESTClient.client('bAsiC','test.com','mlove','123'),_BasicRESTClient)
        self.assertIsInstance(RESTClient.client('BASIC','test.com','mlove','123'),_BasicRESTClient)
"""
class Test_BasicRESTClient(unittest.TestCase):
    def setUp(self):
        self.client = BasicRESTClient('test.com', 'mlove', '123')

    def test__uri_join(self):
        self.assertEqual(self.client._uri_join('/api/v2'),'http://test.com/api/v2')

    def test_SessionConstruction(self):
        self.assertIsInstance(self.client._sess, requests.Session)

    def test_SessionParams(self):
        self.assertEqual(self.client.base, 'test.com')
        self.assertEqual(self.client._sess.auth.username, 'mlove')

        self.assertEqual(self.client._sess.auth.password, '123')

    @patch('requests.Session.request')
    def test_get(self, mock_request):
        r = self.client.request('get','/api/v2',
                                data=json.dumps({'key':'value'}))
        mock_request.assert_called_with(method='get',
                                        url='http://test.com/api/v2',
                                        data=json.dumps({'key':'value'}),
                                        params={})

    @patch('requests.Session.request')
    def test_get_cb(self, mock_request):
        def jsonresp():
            return json.loads(json.dumps({'key':'value'}))

        mock_request.return_value = MagicMock(spec='requests.Response', text={'key':'value'},
                                              status_code=200, json=jsonresp)

        r = self.client.request('get','/api/v2',raise_for_status=False,
                                cb=self.client.strip_data,
                                data=json.dumps({'key':'value'}))

        self.assertEqual(r, {'key':'value'})


    @patch('requests.Session.request')
    def test_post(self, mock_request):
        mock_request.return_value = MagicMock(spec=requests.Response, status_code = 200,
                                              response=json.dumps({'value':'key'}))

        r = self.client.request('post', '/api/v2',
                                data=json.dumps({'key':'value'}))
        mock_request.assert_called_with(method='post',
                                        url='http://test.com/api/v2',
                                        data=json.dumps({'key':'value'}),
                                        params={})
        self.assertIsInstance(r, requests.Response)
        self.assertEqual(r, mock_request.return_value)


    @patch('requests.Session.request')
    def test_post_params(self, mock_request):
        mock_request.return_value = MagicMock(spec=requests.Response, status_code = 200,
                                              response=json.dumps({'value':'key'}))

        r = self.client.request('post', '/api/v2',
                                params={'key':'value'})

        mock_request.assert_called_with(method='post',
                                        url='http://test.com/api/v2',
                                        params={'key':'value'})

        self.assertIsInstance(r, requests.Response)
        self.assertEqual(r, mock_request.return_value)

