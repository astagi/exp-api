from taiga.requestmaker import RequestMaker, RequestMakerException
from taiga.models.base import InstanceResource, ListResource
import taiga.exceptions
import json
import requests
import unittest
from mock import patch

class Fake(InstanceResource):

    endpoint = 'fakes'

    allowed_params = ['param1', 'param2']

    def my_method(self):
        response = self.requester.get('/users/{id}/starred', id=self.id)
        return projects.Projects.parse(response.json(), self.requester)


class Fakes(ListResource):

    instance = Fake


class TestModelBase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @patch('taiga.requestmaker.RequestMaker.put')
    def test_call_model_base_update(self, mock_requestmaker_put):
        rm = RequestMaker('/api/v1', 'fakehost', 'faketoken')
        fake = Fake(rm, id=1, param1='one', param2='two')
        fake.update()
        mock_requestmaker_put.assert_called_once_with('/{endpoint}/{id}', endpoint='fakes',
            id=1, payload=fake.to_dict())

    @patch('taiga.requestmaker.RequestMaker.delete')
    def test_call_model_base_delete(self, mock_requestmaker_delete):
        rm = RequestMaker('/api/v1', 'fakehost', 'faketoken')
        fake = Fake(rm, id=1, param1='one', param2='two')
        fake.delete()
        mock_requestmaker_delete.assert_called_once_with('/{endpoint}/{id}', endpoint='fakes', id=1)

    @patch('taiga.requestmaker.RequestMaker.get')
    def test_call_model_base_get_element(self, mock_requestmaker_get):
        rm = RequestMaker('/api/v1', 'fakehost', 'faketoken')
        fakes = Fakes(rm)
        fakes.get(1)
        mock_requestmaker_get.assert_called_once_with('/{endpoint}/{id}', endpoint='fakes', id=1)

    @patch('taiga.requestmaker.RequestMaker.delete')
    def test_call_model_base_delete_element(self, mock_requestmaker_delete):
        rm = RequestMaker('/api/v1', 'fakehost', 'faketoken')
        fake = Fake(rm, id=1, param1='one', param2='two')
        fake.delete()
        mock_requestmaker_delete.assert_called_once_with('/{endpoint}/{id}', endpoint='fakes', id=1)

    @patch('taiga.requestmaker.RequestMaker.get')
    def test_call_model_base_list_elements(self, mock_requestmaker_get):
        rm = RequestMaker('/api/v1', 'fakehost', 'faketoken')
        fakes = Fakes(rm)
        fakes.list()
        mock_requestmaker_get.assert_called_with('/{endpoint}', endpoint='fakes')
        fakes.list(project_id=1)
        mock_requestmaker_get.assert_called_with('/{endpoint}', endpoint='fakes',
            query={'project_id':1})

    @patch('taiga.models.base.ListResource.list')
    def test_call_model_base_query(self, mock_list):
        rm = RequestMaker('/api/v1', 'fakehost', 'faketoken')
        mock_list.return_value = [
            Fake(rm, param1='param1'),
            Fake(rm, param2='param2'),
            Fake(rm, param1='param1', param2='param2')
        ]
        fakes = Fakes(rm)
        objects = fakes.query(param1='param1')
        self.assertEqual(len(objects), 2)

        objects = fakes.query(param2='param2')
        self.assertEqual(len(objects), 2)

        objects = fakes.query(param1='param1', param2='param2')
        self.assertEqual(len(objects), 1)

        objects = fakes.query(param2='paramfake')
        self.assertEqual(len(objects), 0)
