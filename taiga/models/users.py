from .base import InstanceResource, ListResource
import projects

class User(InstanceResource):

    allowed_params = ['']

    def __str__(self):
        return '{0} ({1})'.format(self.username, self.full_name)

    def delete(self):
        return self.requester.delete('/users/{id}', id=self.id)

    def starred_projects(self):
        response = self.requester.get('/users/{id}/starred', id=self.id)
        return projects.Projects.parse(response.json(), self.requester)


class Users(ListResource):

    instance = User

    def list(self, project_id=''):
        response = self.requester.get('/users')
        return self.parse_list(response.json())

    def get(self, id):
        response = self.requester.get('/users/{id}', id=id)
        return User.parse(self, response.json())
