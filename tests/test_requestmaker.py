from taiga.requestmaker import RequestMaker, RequestMakerException
import json
import unittest
from mock import patch

class MockResponse():
    def __init__(self, status_code, text):
        self.status_code = status_code
        self.text = text

    def json(self):
        return json.loads(self.text)

class TestRequestMaker(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @patch('taiga.requestmaker.requests.get')
    def test_call_requests_get(self, requests_get):
        rm = RequestMaker(api_path='/', host='host', token='f4k3')
        rm.get('/nowhere')
        self.assertTrue(requests_get.called)

    @patch('taiga.requestmaker.requests.post')
    def test_call_requests_post(self, requests_post):
        rm = RequestMaker(api_path='/', host='host', token='f4k3')
        rm.post('/nowhere')
        self.assertTrue(requests_post.called)

    @patch('taiga.requestmaker.requests.put')
    def test_call_requests_put(self, requests_put):
        rm = RequestMaker(api_path='/', host='host', token='f4k3')
        rm.put('/nowhere')
        self.assertTrue(requests_put.called)

    @patch('taiga.requestmaker.requests.delete')
    def test_call_requests_delete(self, requests_delete):
        rm = RequestMaker(api_path='/', host='host', token='f4k3')
        rm.delete('/nowhere')
        self.assertTrue(requests_delete.called)