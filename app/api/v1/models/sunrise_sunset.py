from flask_restful import fields


class SunriseSunset(object):
    sunrise_sunset_fields = {
        "date": fields.String,
        "sunrise": fields.String,
        "sunset": fields.String,
    }

    def __init__(self, date, sunrise, sunset):
        self.date = date
        self.sunrise = sunrise
        self.sunset = sunset


class SunriseSunsetOutput(object):
    sunrise_sunset_output_fields = {
        "data": fields.List(fields.Nested(SunriseSunset.sunrise_sunset_fields)),
        "message": fields.String,
        "success": fields.Boolean,
    }

    def __init__(self, data=None, message="", success=False):
        self.data = data or []
        self.message = message
        self.success = success
