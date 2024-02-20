from flask_restful import fields


class Error(object):
    error_fields = {
        "message": fields.String,
        "success": fields.Boolean,
        "code": fields.Integer,
    }

    def __init__(self, message, code):
        self.message = message
        self.success = False
        self.code = code
