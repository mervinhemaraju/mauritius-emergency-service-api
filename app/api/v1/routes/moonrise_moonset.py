import logging
from flask_restful import Resource, marshal_with
from app.api.v1.services.moonrise_moonset import MoonriseMoonsetService
from app.api.v1.models.moonrise_moonset import MoonriseMoonsetOutput


class MoonriseMoonsetResource(Resource):
    @marshal_with(MoonriseMoonsetOutput.moonrise_moonset_output_fields)
    def get(self, lang):
        output = MoonriseMoonsetOutput()

        try:
            service = MoonriseMoonsetService()
            output.data = service.get_moonrise_moonset()
            output.success = True
            return output, 200

        except Exception as e:
            logging.error(f"Error fetching moonrise/moonset data: {e}")
            output.data = []
            output.message = (
                f"An error occurred while getting moonrise/moonset data: {str(e)}"
            )
            output.success = False
            return output, 404
