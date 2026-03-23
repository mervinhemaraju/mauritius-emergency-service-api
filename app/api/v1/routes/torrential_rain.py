import logging
from flask_restful import Resource, marshal_with
from app.api.v1.services.torrential_rain import TorrentialRainAlertService
from app.api.v1.models.torrential_rain import TorrentialRainAlertOutput
from app.api.v1.services.exceptions import TorrentialRainAlertFailure


class TorrentialRainAlertResource(Resource):
    @marshal_with(TorrentialRainAlertOutput.torrential_rain_alert_output_fields)
    def get(self, lang):
        output = TorrentialRainAlertOutput()

        try:
            hra = TorrentialRainAlertService()
            output.alert = hra.get_alert()
            output.success = True
            return output, 200

        except TorrentialRainAlertFailure as rf:
            logging.error(f"Rainfall Alert error: {rf}")
            output.alert = None
            output.message = "An error occurred while getting the heavy rainfall alert. Please try again later."
            output.success = False
            return output, 404

        except Exception as e:
            logging.error(f"Fatal error while getting rainfall alert: {e}")
            output.alert = None
            output.message = (
                f"An error occurred while getting the heavy rainfall alert: {str(e)}"
            )
            output.success = False
            return output, 404
