import random
import time
from flask_restful import Resource
from flask_restful import marshal_with
from app.api.v1.services.cyclone import Cyclone, CycloneGuidelines
from app.api.v1.models.cyclone_report import CycloneReport
from app.api.v1.models.cyclone_name import CycloneNameOutput
from app.api.v1.models.cyclone_report import CycloneReportOutput
from app.api.v1.models.cyclone_guidelines import CycloneGuidelinesOutput
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


class CycloneReportTestingResource(Resource):
    @marshal_with(CycloneReportOutput.cyclone_report_output_fields)
    # > GET Request
    def get(self, lang):
        # * Create the output object
        output = CycloneReportOutput()

        try:
            # * Generates a random cyclone level
            random_level = random.randint(0, 4)

            # * Creates a fake cyclone news
            fake_news = [
                "This is a fake news.",
                "This is merely for testing purposes.",
                "You can use this in your app to test cyclone levels.",
            ]

            # * Create a fake next bulletin
            fake_bulletin = (
                time.strftime("%H:%M:%S", time.gmtime(random.randint(0, 86399)))
                if random_level != 0
                else None
            )

            # * Update the output object
            output.report = CycloneReport(
                level=random_level,
                next_bulletin=fake_bulletin,
                news=fake_news,
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


class CycloneGuidelinesResource(Resource):
    # > GET Request
    @marshal_with(CycloneGuidelinesOutput.cyclone_guideline_output_fields)
    def get(self, lang):
        # * Create a new cyclone guidelines output object
        output = CycloneGuidelinesOutput()

        try:
            # * Create a new cycloneguideline object
            cyclone = CycloneGuidelines(lang=lang)

            # * Update the output object
            output.guidelines = cyclone.load()
            output.success = True

            # * Return the output object
            return output, 200

        except Exception as e:
            # * Update the output object
            output.message = (
                f"An error occurred while getting the cyclone guidelines: {str(e)}"
            )
            output.guidelines = []
            output.success = False

            # * Return the output object
            return output, 404
