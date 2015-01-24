from .base import InstanceResource, ListResource

class User(InstanceResource):

    endpoint = 'users'

    allowed_params = ['']

    def __str__(self):
        return '{0} ({1})'.format(self.username, self.full_name)

    def starred_projects(self):
        response = self.requester.get('/{endpoint}/{id}/starred', endpoint=self.endpoint, id=self.id)
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
        self.requester.post('/{endpoint}/{id}/star', endpoint=self.endpoint, id=self.id)
        return self

    def unstar(self):
        self.requester.post('/{endpoint}/{id}/unstar', endpoint=self.endpoint, id=self.id)
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
        return UserStory.parse(self.requester, response.json())


class Task(InstanceResource):

    endpoint = 'tasks'

    allowed_params = ['assigned_to', 'blocked_note', 'description', 'is_blocked',
        'is_closed', 'milestone', 'project', 'user_story', 'status', 'subject', 
        'tags', 'us_order', 'taskboard_order', 'is_iocaine','external_reference',
        'watchers']

    def __str__(self):
        return '{0}'.format(self.subject)


class Tasks(ListResource):

    instance = Task

    def create(self, project_id, subject, status, **attrs):
        attrs.update({'project' : project_id, 'subject' : subject, 
            'status' : status})
        response = self.requester.post('/tasks', payload=attrs)
        return Task.parse(self.requester, response.json())


class Attachment(InstanceResource):

    endpoint = 'issues/attachments'

    allowed_params = ['object_id', 'project', 'attached_file', 'description', 'is_deprecated']

    def __str__(self):
        return '{0}'.format(self.subject)


class Attachments(ListResource):

    instance = Attachment

    def __init__(self, requester, issue_project, issue_id):
        super(Attachments, self).__init__(
            requester,
        )
        self.issue_project = issue_project
        self.issue_id = issue_id

    def create(self, subject, attached_file, **attrs):
        attrs.update({'project' : self.issue_project, 'object_id' : self.issue_id})
        response = self.requester.post('/issues/attachments', 
            files={'attached_file' : open(attached_file, 'rb')}, payload=attrs)
        return Attachment.parse(self.requester, response.json())


class Issue(InstanceResource):

    endpoint = 'issues'

    def __init__(self, requester, **params):
        super(Issue, self).__init__(
            requester,
            **params
        )
        self.attachments = Attachments(requester, self.project, self.id)

    allowed_params = ['assigned_to', 'blocked_note', 'description', 'is_blocked',
        'is_closed', 'milestone', 'project', 'status', 'severity', 'priority', 'type',
        'subject', 'tags', 'watchers']

    def upvote(self):
        self.requester.post('/{endpoint}/{id}/upvote', endpoint=self.endpoint, id=self.id)
        return self

    def downvote(self):
        self.requester.post('/{endpoint}/{id}/downvote', endpoint=self.endpoint, id=self.id)
        return self

    def __str__(self):
        return '{0}'.format(self.subject)


class Issues(ListResource):

    instance = Issue

    def create(self, project_id, subject, priority, status, issue_type, severity, **attrs):
        attrs.update({'project' : project_id, 'subject' : subject, 'priority' : priority,
            'status' : status, 'type' : issue_type, 'severity' : severity})
        response = self.requester.post('/issues', payload=attrs)
        return Issue.parse(self.requester, response.json())