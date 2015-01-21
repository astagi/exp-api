import requests
import six

class Resource(object):

    def __init__(self, requester):
        self.requester = requester


class ListResource(Resource):

    def list(self, project_id='', **queryparams):
        if project_id:
            result = self.requester.get('/{endpoint}', endpoint=self.instance.endpoint,
                query={'project_id':project_id})
        else:
            result = self.requester.get('/{endpoint}', endpoint=self.instance.endpoint)
        objects = self.parse_list(result.json())
        result_objects = []
        for obj in objects:
            add = True
            for key, value in six.iteritems(queryparams):
                try:
                    if obj.__dict__[key] != value:
                        add = False
                        break
                except KeyError:
                    add = False
                    break
            if add:
                result_objects.append(obj)
        return result_objects

    def get(self, id):
        response = self.requester.get('/{endpoint}/{id}', endpoint=self.instance.endpoint, id=id)
        return self.instance.parse(self.requester, response.json())

    def delete(self, id):
        self.requester.delete('/{endpoint}/{id}', endpoint=self.instance.endpoint, id=id)
        return self

    @classmethod
    def parse(cls, requester, entries):
        """Parse a JSON array into a list of model instances."""
        result_entries = []
        for entry in entries:
            result_entries.append(cls.instance.parse(requester, entry))
        return result_entries

    def parse_list(self, entries):
        """Parse a JSON array into a list of model instances."""
        result_entries = []
        for entry in entries:
            result_entries.append(self.instance.parse(self.requester, entry))
        return result_entries


class InstanceResource(Resource):

    endpoint = ''

    allowed_params = []

    def __init__(self, requester, **params):
        self.requester = requester
        for key, value in six.iteritems(params):
            setattr(self, key, value)

    def update(self):
        self.requester.put('/{endpoint}/{id}', endpoint=self.endpoint,
            id=self.id, payload=self.to_dict())
        return self

    def delete(self):
        self.requester.delete('/{endpoint}/{id}', endpoint=self.endpoint, id=self.id)
        return self

    def to_dict(self):
        self_dict = {}
        for key, value in six.iteritems(self.__dict__):
            if key in self.allowed_params:
                self_dict[key] = value
        return self_dict

    @classmethod
    def parse(cls, requester, entry):
        """Parse a JSON object into a model instance."""
        if entry is None:
            return ''
        entry_str_dict = dict([(str(key), value) for key, value in entry.items()])
        return cls(requester, **entry_str_dict)

    def __repr__(self):
        return str(self)

    def __str__(self):
        if six.PY3:
            return self.__unicode__()
        else:
            return unicode(self).encode('utf-8')
