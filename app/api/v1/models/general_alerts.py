from flask_restful import fields


class GeneralAlertOutput(object):
    general_alert_output_fields = {
        "alert": fields.String(default=None),
        "message": fields.String,
        "success": fields.Boolean,
    }

    def __init__(self, alert=None, message="", success=False) -> None:
        self.alert = alert
        self.message = message
        self.success = success
