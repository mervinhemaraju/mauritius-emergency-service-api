import logging
from flask_restful import Resource, marshal_with
from app.api.v1.services.sunrise_sunset import SunriseSunsetService
from app.api.v1.models.sunrise_sunset import SunriseSunsetOutput


class SunriseSunsetResource(Resource):
    @marshal_with(SunriseSunsetOutput.sunrise_sunset_output_fields)
    def get(self, lang):
        output = SunriseSunsetOutput()

        try:
            service = SunriseSunsetService()
            output.data = service.get_sunrise_sunset()
            output.success = True
            return output, 200

        except Exception as e:
            logging.error(f"Error fetching sunrise/sunset data: {e}")
            output.data = []
            output.message = (
                f"An error occurred while getting sunrise/sunset data: {str(e)}"
            )
            output.success = False
            return output, 404
