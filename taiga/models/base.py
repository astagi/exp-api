import requests
import six

class Resource(object):

    def __init__(self, requester):
        self.requester = requester


class ListResource(Resource):

    def update(self):
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError

    @classmethod
    def parse(cls, entries, requester):
        """Parse a JSON object into a model instance."""
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

    allowed_params = []

    def __init__(self, requester, **params):
        self.requester = requester
        for key, value in six.iteritems(params):
            setattr(self, key, value)

    def list(self):
        raise NotImplementedError

    def get(self, id):
        raise NotImplementedError

    def delete(self, id):
        raise NotImplementedError

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
