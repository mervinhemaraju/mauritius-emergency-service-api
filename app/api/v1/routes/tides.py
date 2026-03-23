import logging
from flask_restful import Resource, marshal_with
from app.api.v1.services.tides import TidesService
from app.api.v1.models.tides import TidesOutput


class TidesResource(Resource):
    @marshal_with(TidesOutput.tides_output_fields)
    def get(self, lang):
        output = TidesOutput()

        try:
            service = TidesService()
            output.data = service.get_tides()
            output.success = True
            return output, 200

        except Exception as e:
            logging.error(f"Error fetching tides data: {e}")
            output.data = []
            output.message = f"An error occurred while getting tides data: {str(e)}"
            output.success = False
            return output, 404
