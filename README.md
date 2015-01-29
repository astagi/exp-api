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
    host='http://taiga.my.host.org'
)
```

### Create a project

```python
new_project = api.projects.create('TEST PROJECT', 'TESTING API')
```

### Create a new user story

```python
userstory = new_project.add_user_story(
    'New Story', description='Blablablabla'
)
```

You can also create a milestone and pass it to a story

```python
jan_feb_milestone = new_project.add_milestone(
    'MILESTONE 1', '2015-01-26', '2015-02-26'
)

userstory = new_project.add_user_story(
    'New Story', description='Blablablabla',
    milestone=jan_feb_milestone.id
)
```

### Create an issue

```python
newissue = new_project.add_issue(
    'New Issue', new_project.priorities[1].id,
    new_project.issue_statuses[0].id,
    new_project.issue_types[0].id,
    new_project.severities[0].id, description='Bug #5'
)
```

### List elements

```python
projects = api.projects.list()
stories = api.user_stories.list()
```

You can also specify filters

```python
tasks = api.tasks.list(project=1)
```

### Attach a file

You can attach files to issues, user stories and tasks

```python
newissue.attach('Read the README in Issue', 'README.md')
```

### Search

Search function returns a SearchResult object, containing tasks,
user stories and issues:

```python
projects = api.projects.list()
search_result = api.search(projects[0].id, 'NEW')
for user_story in search_result.user_stories:
    print (user_story)
```