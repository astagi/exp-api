import json
import requests

class RequestMakerException(Exception):
    pass

class RequestMaker(object):

    def __init__(self, api_path, host, token):
        self.api_path = api_path
        self.host = host
        self.token = token

    def headers(self):
        headers = {
            'Content-type' : 'application/json',
            'Authorization' : 'Bearer {0}'.format(self.token)
        }
        return headers

    def get(self, uri, **parameters):
        return requests.get(
            self.host + self.api_path + uri.format(**parameters),
            headers=self.headers()
        )

    def post(self, uri, payload=None, **parameters):
        return requests.post(
            self.host + self.api_path + uri.format(**parameters),
            headers=self.headers(),
            data=json.dumps(payload)
        )

    def delete(self, uri, **parameters):
        return requests.delete(
            self.host + self.api_path + uri.format(**parameters),
            headers=self.headers()
        )

    def put(self, uri, payload=None, **parameters):
        return requests.put(
            self.host + self.api_path + uri.format(**parameters),
            headers=self.headers(),
            data=json.dumps(payload)
        )