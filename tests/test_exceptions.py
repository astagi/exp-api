import taiga.exceptions
import unittest


class TestExceptions(unittest.TestCase):

    def test_taiga_rest_exception_parsing(self):
        error_message = '{"_error_type": "taiga.base.exceptions.WrongArguments", "_error_message": "Username or password does not matches user."}'
        taiga_exception = taiga.exceptions.TaigaRestException(
            'uri', 500, error_message)
        self.assertEqual(taiga_exception.message, 'Username or password does not matches user.')

    def test_taiga_rest_exception_parsing_wrong_json(self):
        error_message = 'Plain message error.'
        taiga_exception = taiga.exceptions.TaigaRestException(
            'uri', 500, error_message)
        self.assertEqual(taiga_exception.message, 'Plain message error.')