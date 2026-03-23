from flask_restful import fields


class Tide(object):
    tide_fields = {
        "time": fields.String,
        "height_cm": fields.String,
    }

    def __init__(self, time, height_cm):
        self.time = time
        self.height_cm = height_cm


class TidesEntry(object):
    tides_entry_fields = {
        "date": fields.String,
        "high_tide_1": fields.Nested(Tide.tide_fields, default=None),
        "high_tide_2": fields.Nested(Tide.tide_fields, default=None),
        "low_tide_1": fields.Nested(Tide.tide_fields, default=None),
        "low_tide_2": fields.Nested(Tide.tide_fields, default=None),
    }

    def __init__(self, date, high_tide_1, high_tide_2, low_tide_1, low_tide_2):
        self.date = date
        self.high_tide_1 = high_tide_1
        self.high_tide_2 = high_tide_2
        self.low_tide_1 = low_tide_1
        self.low_tide_2 = low_tide_2


class TidesOutput(object):
    tides_output_fields = {
        "data": fields.List(fields.Nested(TidesEntry.tides_entry_fields)),
        "message": fields.String,
        "success": fields.Boolean,
    }

    def __init__(self, data=None, message="", success=False):
        self.data = data or []
        self.message = message
        self.success = success
