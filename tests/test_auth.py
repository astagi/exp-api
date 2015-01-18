from taiga import TaigaAPI
import json
import unittest
from mock import patch
from .tools import create_mock_json

class MockResponse():
    def __init__(self, status_code, text):
        self.status_code = status_code
        self.text = text

    def json(self):
        return json.loads(self.text)

class TestAuth(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @patch('taiga.client.TaigaAPI._init_resources')
    def test_call_init_if_token_provided(self, init):
        api = TaigaAPI(token='f4k3')
        init.assert_called_once_with()

    @patch('taiga.client.TaigaAPI._init_resources')
    def test_not_call_init_if_no_token_provided(self, init):
        api = TaigaAPI(host='host')
        self.assertFalse(init.called)

    @patch('taiga.client.requests')
    def test_auth_success(self, requests):
        requests.post.return_value = MockResponse(200, create_mock_json('tests/resources/auth_user_success.json'))
        api = TaigaAPI(host='host')
        api.auth('valid_user', 'valid_password')
        self.assertEqual(api.token, 'f4k3')