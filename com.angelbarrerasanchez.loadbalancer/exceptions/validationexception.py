class validationexceptions(Exception):
    def __init__(self, errorcode, message, statuscode=400):
        self.statuscode = statuscode
        self.message = message
        self.errorcode = errorcode

    def to_dict(self):
        rv = dict()
        rv['status_code'] = self.statuscode
        rv['error'] = self.errorcode
        rv['description'] = self.message
        return rv