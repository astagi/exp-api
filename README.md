python-taiga
============

A module for using the [Taiga REST API](http://taigaio.github.io/taiga-doc/dist/api.html "Taiga REST API documentation").

## Getting Started

Getting started with the Taiga API couldn't be easier. Create a
`TaigaAPI` and you're ready to go.

### API Credentials

The `TaigaAPI` needs your Taiga credentials. You can pass these
directly to the auth method (see the code below).

```python
from taiga import TaigaAPI

api = TaigaAPI()

api.auth(
    username='user',
    password='psw'
)
```

Alternately, you can pass a token to the constructor `TaigaAPI` constructor.

```python
from taiga import TaigaAPI

api = TaigaAPI(token='mytoken')
```

You can also specify a different host if you use Taiga somewhere else

```python
from taiga import TaigaAPI

api = TaigaAPI(
    host='http://taiga.nph.nephila.it'
)
```

### List all the users

```python
from taiga import TaigaAPI

api = TaigaAPI(token='token')

print (api.users.list())
```

You can pass a `project_id` parameter to get all the users of a specific project.

```python
print (api.users.list(project_id=1))
```

### Update an user

```python
user.full_name = 'Andreas'
user.update()
```

### Delete an user

```python
user.delete()
```

### List all the projects

```python
from taiga import TaigaAPI

api = TaigaAPI(token='token')

print (api.projects.list())
```

### Get all the users in a project

```python
from taiga import TaigaAPI

api = TaigaAPI(token='token')

for user in projects[0].users:
    print (user)
```

### Create a project

```python
new_project = api.projects.create('TEST PROJECT', 'TESTING API')
```

### Star a project

```python
new_project.star()
```

### Update a project

You can change any attribute and then call update

```python
new_project.name = 'New project'
new_project.update()
```

### Delete a project

```python
new_project.delete()
```

### Use me object

me is a User object representing you

```python
from taiga import TaigaAPI

api = TaigaAPI(token='token')

print (api.me)
print (api.me.starred_projects())
```

### Create an user story

api.me provides a User object representing you

```python
from taiga import TaigaAPI

api = TaigaAPI(token='token')

new_project = api.projects.create('TEST PROJECT', 'TESTING API')
new_story = api.stories.create(new_project.id, 'New Story', description='Blablablabla')
```

### List all the stories

```python
from taiga import TaigaAPI

api = TaigaAPI(token='token')

stories = api.stories.list()
print (stories)
```

You can pass a `project_id` parameter to get all the user stories of a specific project.

```python
stories = api.stories.list(project_id=1)
print (stories)
```

### Update a story

```python
new_story.description = 'New description'
new_story.update()
```

### Delete a story

```python
new_story = api.stories.create(new_project.id, 'New Story', description='Blablablabla')
new_story.delete()
```