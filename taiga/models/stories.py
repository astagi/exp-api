from .base import InstanceResource, ListResource
from .users import User

class Story(InstanceResource):

    allowed_params = ['assigned_to', 'backlog_order', 'blocked_note',
        'client_requirement', 'description', 'is_archived', 'is_blocked',
        'is_closed', 'kanban_order', 'milestone', 'points', 'project',
        'sprint_order', 'status', 'subject', 'tags', 'team_requirement',
        'watchers']

    def __str__(self):
        return '{0}'.format(self.subject)

    def update(self):
        return self.requester.put('/userstories/{id}', id=self.id, payload=self.to_dict())

    def delete(self):
        return self.requester.delete('/userstories/{id}', id=self.id)


class Stories(ListResource):

    instance = Story

    def list(self, project_id=''):
        if project_id:
            response = self.requester.get('/userstories', query={'project_id':project_id})
        else:
            response = self.requester.get('/userstories')
        return self.parse_list(response.json())

    def get(self, id):
        response = self.requester.get('/userstories/{id}', id=id)
        return Story.parse(self, response.json())

    def create(self, project_id, subject, **attrs):
        attrs.update({'project' : project_id, 'subject' : subject})
        response = self.requester.post('/userstories', payload=attrs)
        return Story.parse(self, response.json())
