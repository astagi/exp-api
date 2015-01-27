from taiga.requestmaker import RequestMaker, RequestMakerException
from taiga.models.base import InstanceResource, ListResource
from taiga import TaigaAPI
import taiga.exceptions
import json
import requests
import unittest
from mock import patch
from .tools import create_mock_json
from .tools import MockResponse

class TestUsers(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @unittest.skip
    @patch('taiga.requestmaker.RequestMaker.get')
    def test_single_user_parsing(self, mock_requestmaker_get):
        mock_requestmaker_get.return_value = MockResponse(200,
            create_mock_json('tests/resources/user_details_success.json'))
        api = TaigaAPI(token='f4k3')
        user = api.users.get(1)
        self.assertEqual(user.username, 'astagi')

    @unittest.skip
    @patch('taiga.requestmaker.RequestMaker.get')
    def test_list_users_parsing(self, mock_requestmaker_get):
        mock_requestmaker_get.return_value = MockResponse(200,
            create_mock_json('tests/resources/users_list_success.json'))
        api = TaigaAPI(token='f4k3')
        users = api.users.list()
        self.assertEqual(users[0].username, 'astagi')
        self.assertEqual(len(users), 1)

