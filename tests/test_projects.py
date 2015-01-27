from taiga.requestmaker import RequestMaker, RequestMakerException
from taiga.models.base import InstanceResource, ListResource
from taiga.models import User, Point, UserStoryStatus, Severity
from taiga import TaigaAPI
import taiga.exceptions
import json
import requests
import unittest
from mock import patch
from .tools import create_mock_json
from .tools import MockResponse

class TestProjects(unittest.TestCase):

    @patch('taiga.requestmaker.RequestMaker.get')
    def test_single_project_parsing(self, mock_requestmaker_get):
        mock_requestmaker_get.return_value = MockResponse(200,
            create_mock_json('tests/resources/project_details_success.json'))
        api = TaigaAPI(token='f4k3')
        project = api.projects.get(1)
        self.assertEqual(project.description, 'test 1 on real taiga')
        self.assertEqual(len(project.users), 1)
        self.assertTrue(isinstance(project.points[0], Point))
        self.assertTrue(isinstance(project.us_statuses[0], UserStoryStatus))
        self.assertTrue(isinstance(project.severities[0], Severity))

    @patch('taiga.requestmaker.RequestMaker.get')
    def test_list_projects_parsing(self, mock_requestmaker_get):
        mock_requestmaker_get.return_value = MockResponse(200,
            create_mock_json('tests/resources/projects_list_success.json'))
        api = TaigaAPI(token='f4k3')
        projects = api.projects.list()
        self.assertEqual(projects[0].description, 'test 1 on real taiga')
        self.assertEqual(len(projects), 1)
        self.assertEqual(len(projects[0].users), 1)
        self.assertTrue(isinstance(projects[0].users[0], User))
