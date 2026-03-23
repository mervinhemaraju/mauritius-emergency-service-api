from flask_restful import fields


class TorrentialRainAlert(object):
    torrential_rain_alert_fields = {
        "title": fields.String,
    }

    def __init__(self, title) -> None:
        self.title = title


class TorrentialRainAlertOutput(object):
    torrential_rain_alert_output_fields = {
        "alert": fields.Nested(
            TorrentialRainAlert.torrential_rain_alert_fields, default=None
        ),
        "message": fields.String,
        "success": fields.Boolean,
    }

    def __init__(self, alert=None, message="", success=False) -> None:
        self.alert = alert
        self.message = message
        self.success = success
