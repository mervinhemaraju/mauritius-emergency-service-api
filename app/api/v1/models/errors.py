from flask_restful import fields


class Error(object):
    error_fields = {
        "message": fields.String,
        "status": fields.Boolean,
        "code": fields.Integer,
    }

    def __init__(self, message, status, code):
        self.message = message
        self.status = status
        self.code = code
