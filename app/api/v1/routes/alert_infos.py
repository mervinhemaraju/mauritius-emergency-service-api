import logging
from flask_restful import Resource, marshal_with
from app.api.v1.services.torrential_rain_precautions import (
    TorrentialRainPrecautionsService,
)
from app.api.v1.services.torrential_rain_warnings import TorrentialRainWarningsService
from app.api.v1.services.tsunami_precautions import TsunamiPrecautionsService
from app.api.v1.services.tsunami_warnings import TsunamiWarningsService
from app.api.v1.models.torrential_rain_precautions import (
    TorrentialRainPrecautionsOutput,
)
from app.api.v1.models.torrential_rain_warnings import TorrentialRainWarningsOutput
from app.api.v1.models.tsunami_precautions import TsunamiPrecautionsOutput
from app.api.v1.models.tsunami_warnings import TsunamiWarningsOutput


class TorrentialRainPrecautionsResource(Resource):
    @marshal_with(
        TorrentialRainPrecautionsOutput.torrential_rain_precautions_output_fields
    )
    def get(self, lang):
        output = TorrentialRainPrecautionsOutput()
        try:
            output.data = TorrentialRainPrecautionsService(lang).load()
            output.success = True
            return output, 200
        except Exception as e:
            logging.error(f"Error loading torrential rain precautions: {e}")
            output.message = (
                f"An error occurred while getting torrential rain precautions: {str(e)}"
            )
            output.success = False
            return output, 404


class TorrentialRainWarningsResource(Resource):
    @marshal_with(TorrentialRainWarningsOutput.torrential_rain_warnings_output_fields)
    def get(self, lang):
        output = TorrentialRainWarningsOutput()
        try:
            output.data = TorrentialRainWarningsService(lang).load()
            output.success = True
            return output, 200
        except Exception as e:
            logging.error(f"Error loading torrential rain warnings: {e}")
            output.message = (
                f"An error occurred while getting torrential rain warnings: {str(e)}"
            )
            output.success = False
            return output, 404


class TsunamiPrecautionsResource(Resource):
    @marshal_with(TsunamiPrecautionsOutput.tsunami_precautions_output_fields)
    def get(self, lang):
        output = TsunamiPrecautionsOutput()
        try:
            output.data = TsunamiPrecautionsService(lang).load()
            output.success = True
            return output, 200
        except Exception as e:
            logging.error(f"Error loading tsunami precautions: {e}")
            output.message = (
                f"An error occurred while getting tsunami precautions: {str(e)}"
            )
            output.success = False
            return output, 404


class TsunamiWarningsResource(Resource):
    @marshal_with(TsunamiWarningsOutput.tsunami_warnings_output_fields)
    def get(self, lang):
        output = TsunamiWarningsOutput()
        try:
            output.data = TsunamiWarningsService(lang).load()
            output.success = True
            return output, 200
        except Exception as e:
            logging.error(f"Error loading tsunami warnings: {e}")
            output.message = (
                f"An error occurred while getting tsunami warnings: {str(e)}"
            )
            output.success = False
            return output, 404
