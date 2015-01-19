class TaigaException(Exception):
    pass

class TaigaRestException(TaigaException):

    def __init__(self, uri, status_code, msg="", method='GET'):
        self.uri = uri
        self.msg = msg
        self.status_code = status_code
        self.method = method
