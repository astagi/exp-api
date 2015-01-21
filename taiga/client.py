import json
import requests
from .models import Projects, UserStories, Users, User
from .requestmaker import RequestMaker
from requests.exceptions import RequestException
from . import exceptions

class TaigaAPI:

    def __init__(self, host='https://api.taiga.io', token=None):
        self.host = host
        self.token = token
        if token:
            self.raw_request = RequestMaker('/api/v1', self.host, self.token)
            self._init_resources()

    def _init_resources(self):
        self.me.requester = self.raw_request
        self.projects = Projects(self.raw_request)
        self.userstories = UserStories(self.raw_request)
        self.users = Users(self.raw_request)

    def auth(self, username, password):
        headers = {
            'Content-type': 'application/json'
        }
        payload = {
            'type' : 'normal',
            'username' : username,
            'password' : password
        }
        try:
            full_url = self.host + '/api/v1/auth'
            response = requests.post(
                full_url,
                data=json.dumps(payload),
                headers=headers
            )
        except RequestException as e:
            raise exceptions.TaigaRestException(full_url, 400, 'Network error!', 'GET')
        if response.status_code != 200:
            raise exceptions.TaigaRestException(full_url, response.status_code, response.text, 'GET')
        self.token = response.json()['auth_token']
        self.raw_request = RequestMaker('/api/v1', self.host, self.token)
        self.me = User.parse(self.raw_request, response.json())
        self._init_resources()
