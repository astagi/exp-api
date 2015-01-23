from .base import InstanceResource, ListResource

class User(InstanceResource):

    endpoint = 'users'

    allowed_params = ['']

    def __str__(self):
        return '{0} ({1})'.format(self.username, self.full_name)

    def starred_projects(self):
        response = self.requester.get('/users/{id}/starred', id=self.id)
        return Projects.parse(self.requester, response.json())


class Users(ListResource):

    instance = User


class Project(InstanceResource):

    endpoint = 'projects'

    allowed_params = ['name', 'description', 'creation_template', 'is_backlog_activated',
        'is_issues_activated', 'is_kanban_activated', 'is_private', 'is_wiki_activated',
        'videoconferences', 'videoconferences_salt', 'total_milestones',
        'total_story_points']

    parser = {'users' : Users}

    def __str__(self):
        return '{0}'.format(self.name)

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


class UserStory(InstanceResource):

    endpoint = 'userstories'

    allowed_params = ['assigned_to', 'backlog_order', 'blocked_note',
        'client_requirement', 'description', 'is_archived', 'is_blocked',
        'is_closed', 'kanban_order', 'milestone', 'points', 'project',
        'sprint_order', 'status', 'subject', 'tags', 'team_requirement',
        'watchers']

    def __str__(self):
        return '{0}'.format(self.subject)


class UserStories(ListResource):

    instance = UserStory

    def create(self, project_id, subject, **attrs):
        attrs.update({'project' : project_id, 'subject' : subject})
        response = self.requester.post('/userstories', payload=attrs)
        return Story.parse(self, response.json())
