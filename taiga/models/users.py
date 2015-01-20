from .base import InstanceResource, ListResource
import projects

class User(InstanceResource):

    endpoint = 'users'

    allowed_params = ['']

    def __str__(self):
        return '{0} ({1})'.format(self.username, self.full_name)

    def starred_projects(self):
        response = self.requester.get('/users/{id}/starred', id=self.id)
        return projects.Projects.parse(self.requester, response.json())


class Users(ListResource):

    instance = User
