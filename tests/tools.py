from mock import Mock


def create_mock_json(path):
    with open(path) as f:
        return f.read()