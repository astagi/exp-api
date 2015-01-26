import datetime
from .base import InstanceResource, ListResource

class User(InstanceResource):

    endpoint = 'users'

    def __str__(self):
        return '{0} ({1})'.format(self.username, self.full_name)

    def starred_projects(self):
        response = self.requester.get('/{endpoint}/{id}/starred', endpoint=self.endpoint, id=self.id)
        return Projects.parse(self.requester, response.json())


class Users(ListResource):

    instance = User


class Priority(InstanceResource):

    endpoint = 'priorities'

    allowed_params = ['name', 'color', 'order', 'project']

    def __str__(self):
        return '{0}'.format(self.name)


class Priorities(ListResource):

    instance = Priority

    def create(self, project_id, name, **attrs):
        attrs.update({'project' : project_id, 'name' : name})
        response = self.requester.post('/{endpoint}', endpoint=self.instance.endpoint,
            payload=attrs)
        return self.instance.parse(self.requester, response.json())


class Attachment(InstanceResource):

    allowed_params = ['object_id', 'project', 'attached_file', 'description', 'is_deprecated']

    def __str__(self):
        return '{0}'.format(self.subject)


class Attachments(ListResource):

    def create(self, project_id, object_id, subject, attached_file, **attrs):
        attrs.update({'project' : project_id, 'object_id' : object_id})
        response = self.requester.post('/{endpoint}', endpoint=self.instance.endpoint,
            files={'attached_file' : open(attached_file, 'rb')}, payload=attrs)
        return self.instance.parse(self.requester, response.json())


class UserStoryAttachment(Attachment):

    endpoint = 'userstories/attachments'


class UserStoryAttachments(Attachments):

    instance = UserStoryAttachment


class UserStory(InstanceResource):

    endpoint = 'userstories'

    allowed_params = ['assigned_to', 'backlog_order', 'blocked_note',
        'client_requirement', 'description', 'is_archived', 'is_blocked',
        'is_closed', 'kanban_order', 'milestone', 'points', 'project',
        'sprint_order', 'status', 'subject', 'tags', 'team_requirement',
        'watchers']

    def add_task(self, subject, status, **attrs):
        return Tasks(self.requester).create(self.project, subject, status, user_story=self.id)

    def list_tasks():
        return Tasks(self.requester).list()

    def attach(self, subject, attached_file, **attrs):
        return UserStoryAttachments(self.requester).create(self.project, self.id,
            subject, attached_file, **attrs)

    def __str__(self):
        return '{0}'.format(self.subject)


class UserStories(ListResource):

    instance = UserStory

    def create(self, project_id, subject, **attrs):
        attrs.update({'project' : project_id, 'subject' : subject})
        response = self.requester.post('/userstories', payload=attrs)
        return UserStory.parse(self.requester, response.json())


class Milestone(InstanceResource):

    endpoint = 'milestones'

    allowed_params = ['name', 'project', 'estimated_start', 'estimated_finish',
        'disponibility', 'slug', 'order', 'watchers']

    parser = {
        'user_stories' : UserStories,
    }

    def __str__(self):
        return '{0}'.format(self.name)


class Milestones(ListResource):

    instance = Milestone

    def create(self, project_id, name, estimated_start, estimated_finish, **attrs):
        if isinstance(estimated_start, datetime.datetime):
            estimated_start = estimated_start.strftime('%Y-%m-%d')
        if isinstance(estimated_finish, datetime.datetime):
            estimated_finish = estimated_finish.strftime('%Y-%m-%d')
        attrs.update({
            'project' : project_id,
            'name' : name,
            'estimated_start' : estimated_start,
            'estimated_finish' : estimated_finish
        })
        response = self.requester.post('/{endpoint}', endpoint=self.instance.endpoint,
            payload=attrs)
        return self.instance.parse(self.requester, response.json())


class TaskStatus(InstanceResource):

    endpoint = 'task-statuses'

    allowed_params = ['name', 'color', 'order', 'project', 'is_closed']

    def __str__(self):
        return '{0}'.format(self.name)


class TaskStatuses(ListResource):

    instance = TaskStatus

    def create(self, project_id, name, **attrs):
        attrs.update({'project' : project_id, 'name' : name})
        response = self.requester.post('/{endpoint}', endpoint=self.instance.endpoint,
            payload=attrs)
        return self.instance.parse(self.requester, response.json())


class TaskAttachment(Attachment):

    endpoint = 'tasks/attachments'


class TaskAttachments(Attachments):

    instance = TaskAttachment


class Task(InstanceResource):

    endpoint = 'tasks'

    allowed_params = ['assigned_to', 'blocked_note', 'description', 'is_blocked',
        'is_closed', 'milestone', 'project', 'user_story', 'status', 'subject',
        'tags', 'us_order', 'taskboard_order', 'is_iocaine','external_reference',
        'watchers']

    def attach(self, subject, attached_file, **attrs):
        return TaskAttachments(self.requester).create(self.project, self.id,
            subject, attached_file, **attrs)

    def __str__(self):
        return '{0}'.format(self.subject)


class Tasks(ListResource):

    instance = Task

    def create(self, project_id, subject, status, **attrs):
        attrs.update({'project' : project_id, 'subject' : subject,
            'status' : status})
        response = self.requester.post('/tasks', payload=attrs)
        return Task.parse(self.requester, response.json())


class IssueType(InstanceResource):

    endpoint = 'issue-statuses'

    allowed_params = ['name', 'color', 'order', 'project']

    def __str__(self):
        return '{0}'.format(self.name)


class IssueTypes(ListResource):

    instance = IssueType

    def create(self, project_id, name, **attrs):
        attrs.update({'project' : project_id, 'name' : name})
        response = self.requester.post('/{endpoint}', endpoint=self.instance.endpoint,
            payload=attrs)
        return self.instance.parse(self.requester, response.json())


class IssueStatus(InstanceResource):

    endpoint = 'issue-statuses'

    allowed_params = ['name', 'color', 'order', 'project', 'is_closed']

    def __str__(self):
        return '{0}'.format(self.name)


class IssueStatuses(ListResource):

    instance = IssueStatus

    def create(self, project_id, name, **attrs):
        attrs.update({'project' : project_id, 'name' : name})
        response = self.requester.post('/{endpoint}', endpoint=self.instance.endpoint,
            payload=attrs)
        return self.instance.parse(self.requester, response.json())


class IssueAttachment(Attachment):

    endpoint = 'issues/attachments'


class IssueAttachments(Attachments):

    instance = IssueAttachment


class Issue(InstanceResource):

    endpoint = 'issues'

    allowed_params = ['assigned_to', 'blocked_note', 'description', 'is_blocked',
        'is_closed', 'milestone', 'project', 'status', 'severity', 'priority', 'type',
        'subject', 'tags', 'watchers']

    def upvote(self):
        self.requester.post('/{endpoint}/{id}/upvote', endpoint=self.endpoint, id=self.id)
        return self

    def downvote(self):
        self.requester.post('/{endpoint}/{id}/downvote', endpoint=self.endpoint, id=self.id)
        return self

    def attach(self, subject, attached_file, **attrs):
        return IssueAttachments(self.requester).create(self.project, self.id,
            subject, attached_file, **attrs)

    def __str__(self):
        return '{0}'.format(self.subject)


class Issues(ListResource):

    instance = Issue

    def create(self, project_id, subject, priority, status, issue_type, severity, **attrs):
        attrs.update({'project' : project_id, 'subject' : subject, 'priority' : priority,
            'status' : status, 'type' : issue_type, 'severity' : severity})
        response = self.requester.post('/issues', payload=attrs)
        return Issue.parse(self.requester, response.json())


class Severity(InstanceResource):

    endpoint = 'severities'

    allowed_params = ['name', 'color', 'order', 'project']
    def __str__(self):
        return '{0}'.format(self.name)


class Severities(ListResource):

    instance = Severity

    def create(self, project_id, name, **attrs):
        attrs.update({'project' : project_id, 'name' : name})
        response = self.requester.post('/{endpoint}', endpoint=self.instance.endpoint,
            payload=attrs)
        return self.instance.parse(self.requester, response.json())


class Project(InstanceResource):

    endpoint = 'projects'

    allowed_params = ['name', 'description', 'creation_template', 'is_backlog_activated',
        'is_issues_activated', 'is_kanban_activated', 'is_private', 'is_wiki_activated',
        'videoconferences', 'videoconferences_salt', 'total_milestones',
        'total_story_points']

    parser = {
        'users' : Users,
        'priorities' : Priorities,
        'issue_statuses' : IssueStatuses,
        'issue_types' : IssueTypes,
        'task_statuses' : TaskStatuses,
        'severities' : Severities
    }

    def __str__(self):
        return '{0}'.format(self.name)

    def star(self):
        self.requester.post('/{endpoint}/{id}/star', endpoint=self.endpoint, id=self.id)
        return self

    def unstar(self):
        self.requester.post('/{endpoint}/{id}/unstar', endpoint=self.endpoint, id=self.id)
        return self

    def add_user_story(self, subject, **attrs):
        return UserStories(self.requester).create(self.id, subject, **attrs)

    def list_user_stories(self):
        return UserStories(self.requester).list(self.id)

    def add_issue(self, subject, priority, status, issue_type, severity, **attrs):
        return Issues(self.requester).create(self.id, subject,
            priority, status, issue_type, severity, **attrs)

    def list_issues(self):
        return Issues(self.requester).list(self.id)

    def add_milestone(self, name, estimated_start, estimated_finish, **attrs):
        return Milestones(self.requester).create(self.id, name,
            estimated_start, estimated_finish, **attrs)

    def list_milestones(self):
        return Milestones(self.requester).list(self.id)

class Projects(ListResource):

    instance = Project

    def create(self, name, description, **attrs):
        attrs.update({'name' : name, 'description' : description})
        response = self.requester.post('/projects', payload=attrs)
        return Project.parse(self.requester, response.json())
