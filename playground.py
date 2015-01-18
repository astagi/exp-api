from taiga import TaigaAPI

api = TaigaAPI(
    host='http://taiga.nph.nephila.it'
)

api.auth(
    username='user',
    password='psw'
)

projects = api.projects.list()

print projects

for user in projects[0].users:
    print user

stories = api.stories.list()
print stories

print api.me

projects[0].star()
print api.me.starred_projects()

new_project = api.projects.create('TEST PROJECT', 'TESTING API')
new_project.name = 'TEST PROJECT 2'
new_project.update()

api.stories.create(new_project.id, 'New Story', description='Blablablabla')

new_project.delete()