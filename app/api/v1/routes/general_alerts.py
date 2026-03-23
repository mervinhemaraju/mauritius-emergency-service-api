import logging
from flask_restful import Resource, marshal_with
from app.api.v1.services.general_alerts import GeneralAlertService
from app.api.v1.models.general_alerts import GeneralAlertOutput
from app.api.v1.services.exceptions import GeneralAlertFailure


class GeneralAlertResource(Resource):
    @marshal_with(GeneralAlertOutput.general_alert_output_fields)
    def get(self, lang):
        output = GeneralAlertOutput()

        try:
            service = GeneralAlertService()
            output.alert = service.get_alert()
            output.success = True
            return output, 200

        except GeneralAlertFailure as e:
            logging.error(f"General alert error: {e}")
            output.alert = None
            output.message = "An error occurred while getting the general alert. Please try again later."
            output.success = False
            return output, 404

        except Exception as e:
            logging.error(f"Fatal error while getting general alert: {e}")
            output.alert = None
            output.message = (
                f"An error occurred while getting the general alert: {str(e)}"
            )
            output.success = False
            return output, 404
