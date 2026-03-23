from flask_restful import fields


class MoonriseMoonset(object):
    moonrise_moonset_fields = {
        "date": fields.String,
        "phase": fields.String,
        "moonrise": fields.String,
        "moonset": fields.String,
    }

    def __init__(self, date, phase, moonrise, moonset):
        self.date = date
        self.phase = phase
        self.moonrise = moonrise
        self.moonset = moonset


class MoonriseMoonsetOutput(object):
    moonrise_moonset_output_fields = {
        "data": fields.List(fields.Nested(MoonriseMoonset.moonrise_moonset_fields)),
        "message": fields.String,
        "success": fields.Boolean,
    }

    def __init__(self, data=None, message="", success=False):
        self.data = data or []
        self.message = message
        self.success = success
