import json
import requests
from .models import Projects, Stories, Users, User
from .requestmaker import RequestMaker

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
        self.stories = Stories(self.raw_request)
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
        response = requests.post(
            self.host + '/api/v1/auth',
            data=json.dumps(payload),
            headers=headers
        )
        self.token = response.json()['auth_token']
        self.raw_request = RequestMaker('/api/v1', self.host, self.token)
        self.me = User.parse(self.raw_request, response.json())
        self._init_resources()