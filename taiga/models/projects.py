from .base import InstanceResource, ListResource
import users

class Project(InstanceResource):

    endpoint = 'projects'

    allowed_params = ['name', 'description', 'creation_template', 'is_backlog_activated',
        'is_issues_activated', 'is_kanban_activated', 'is_private', 'is_wiki_activated',
        'videoconferences', 'videoconferences_salt', 'total_milestones',
        'total_story_points']

    def __str__(self):
        return '{0}'.format(self.name)

    @classmethod
    def parse(cls, requester, entry):
        if 'users' in entry:
            entry['users'] = users.Users.parse(requester, entry['users'])
        return Project(requester, **entry)

    def star(self):
        self.requester.post('/projects/{id}/star', id=self.id)
        return self

    def unstar(self):
        self.requester.post('/projects/{id}/unstar', id=self.id)
        return self


class Projects(ListResource):

    instance = Project

    def create(self, name, description, **attrs):
        attrs.update({'name' : name, 'description' : description})
        response = self.requester.post('/projects', payload=attrs)
        return Project.parse(self.requester, response.json())
