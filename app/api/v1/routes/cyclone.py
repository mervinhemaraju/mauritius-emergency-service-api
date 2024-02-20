from flask_restful import Resource
from flask_restful import marshal_with
from app.api.v1.services.cyclone import Cyclone
from app.api.v1.models.cyclone_report import CycloneReport
from app.api.v1.models.cyclone_name import CycloneNameOutput
from app.api.v1.models.cyclone_report import CycloneReportOutput
from app.api.v1.utils.constants import cyclone_names_url_def


class CycloneReportResource(Resource):
    @marshal_with(CycloneReportOutput.cyclone_report_output_fields)
    # > GET Request
    def get(self, lang):
        # * Create the output object
        output = CycloneReportOutput()

        try:
            # * Create a new cyclone object
            cyclone = Cyclone(lang=lang)

            # * Update the output object
            output.report = CycloneReport(
                level=cyclone.class_level(),
                next_bulletin=cyclone.next_bulletin(),
                news=cyclone.news(),
            )
            output.success = True

            # * Return the output object
            return output, 200
        except Exception as e:
            # * Update the output object
            output.report = None
            output.message = (
                f"An error occurred while getting the cyclone report: {str(e)}"
            )

            # * Return the output object
            return output, 404


class CycloneNamesResource(Resource):
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
