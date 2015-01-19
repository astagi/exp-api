from .base import InstanceResource, ListResource
import users

class Project(InstanceResource):

    allowed_params = ['name', 'description', 'creation_template', 'is_backlog_activated',
        'is_issues_activated', 'is_kanban_activated', 'is_private', 'is_wiki_activated',
        'videoconferences', 'videoconferences_salt', 'total_milestones',
        'total_story_points']

    def __str__(self):
        return '{0}'.format(self.name)

    @classmethod
    def parse(cls, requester, entry):
        if 'users' in entry:
            entry['users'] = users.Users.parse(entry['users'], requester)
        return Project(requester, **entry)

    def update(self):
        self.requester.put('/projects/{id}', id=self.id, payload=self.to_dict())
        return self

    def delete(self):
        self.requester.delete('/projects/{id}', id=self.id)
        return self

    def star(self):
        self.requester.post('/projects/{id}/star', id=self.id)
        return self

    def unstar(self):
        self.requester.post('/projects/{id}/unstar', id=self.id)
        return self


class Projects(ListResource):

    instance = Project

    def list(self):
        response = self.requester.get('/projects')
        return self.parse_list(response.json())

    def get(self, id):
        response = self.requester.get('/projects/{id}', id=id)
        return Projects.parse(self.requester, response.json())

    def create(self, name, description, **attrs):
        attrs.update({'name' : name, 'description' : description})
        response = self.requester.post('/projects', payload=attrs)
        return Project.parse(self.requester, response.json())
