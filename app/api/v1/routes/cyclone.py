from flask_restful import Resource
from flask_restful import marshal_with, fields
from app.api.v1.services.cyclone import Cyclone
from app.api.v1.models.cyclone_name import CycloneNameOutput
from app.messages.messages import (
    CONTENT_NOT_FOUND_REPORT,
    CONTENT_NOT_FOUND_NAMES,
    content_cyclone_report,
    content_cyclone_names,
)
from app.api.v1.utils.constants import cyclone_names_url_def


class CycloneReport(Resource):
    # > GET Request
    def get(self, lang):
        try:
            # * Create a new cyclone object
            cyclone = Cyclone(lang=lang)

            # * Create a cyclone report
            return (
                content_cyclone_report(
                    level=cyclone.class_level(),
                    next_bulletin=cyclone.next_bulletin(),
                    news=cyclone.news(),
                ),
                200,
            )
        except Exception as e:
            # * Update the content message
            error_content = CONTENT_NOT_FOUND_REPORT
            error_content["message"] = error_content["message"].format(str(e))
            return (error_content, 404)


class CycloneNames(Resource):
    # > GET Request
    @marshal_with(CycloneNameOutput.cyclone_name_output_fields)
    def get(self, lang):
        # * Create a new cyclone name output object
        output = CycloneNameOutput()

        try:
            # * Create a new cyclone object
            cyclone = Cyclone(lang=lang, url=cyclone_names_url_def)

            # * Update the output object
            output.names = cyclone.names()
            output.success = True

            # * Return the output object
            return output, 200

        except Exception as e:
            # * Update the output object
            output.message = (
                f"An error occurred while getting the cyclone names: {str(e)}"
            )
            output.names = []
            output.success = False

            # * Return the output object
            return output, 404
