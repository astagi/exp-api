from taiga import TaigaAPI

api = TaigaAPI(
    #host='http://taiga.nph.nephila.it'
)

api.auth(
    username='usr',
    password='psw'
)

new_project = api.projects.create('TEST PROJECT', 'TESTING API')

new_project.name = 'TEST PROJECT 2'
new_project.update()

userstory = new_project.add_user_story('New Story', description='Blablablabla')
userstory.attach('Read the README in User Story', 'README.md')

userstory.add_task('New Task 2', new_project.task_statuses[0].id).attach('Read the README in Task', 'README.md')

newissue = new_project.add_issue('New Issue', new_project.priorities[1].id, 
	new_project.issue_statuses[0].id,
	new_project.issue_types[0].id,
	new_project.severities[0].id, description='Bug #5')
newissue.attach('Read the README in Issue', 'README.md')

"""
users = api.users.list()
print (users)

projects = api.projects.list()
print (projects)

for user in projects[0].users:
    print (user)

stories = api.userstories.list()
print (stories)

projects[0].star()
"""