import logging
from flask_restful import Resource
from flask_restful import marshal_with
from app.api.v1.services.ceb import Ceb
from app.api.v1.models.ceb_outage import CebOutagesOutput, CebOutagesByDistrictOutput
from app.api.v1.services.exceptions import CebOutagesFailure


class CebOutages(Resource):
    @marshal_with(CebOutagesOutput.ceb_outages_output_fields)
    def get(self, lang):
        try:
            # Create a new ceb class
            ceb = Ceb()

            # Get the list of outages
            district_outages_list = ceb.get_outages()

            # Return success response
            return CebOutagesOutput(
                district_outages=district_outages_list,
                success=True,
            )

        except CebOutagesFailure as cf:
            # Log the error
            logging.error(f"CEB Outages error: {cf}")

            # Return the output
            return CebOutagesOutput(
                district_outages=[],
                message="An error occurred while getting the CEB outages. Please try again later.",
                success=False,
            )
        except Exception as e:
            # Log the error
            print(f"Fatal error while getting ceb outages: {e}")

            # Return the output
            return CebOutagesOutput(
                district_outages=[],
                message="An error occurred while getting the CEB outages. Please try again later.",
                success=False,
            )


class CebOutagesByDistrict(Resource):
    @marshal_with(CebOutagesByDistrictOutput.ceb_outages_by_district_output_fields)
    def get(self, lang, district):
        try:
            # Create a new ceb class
            ceb = Ceb()

            # Get the list of outages
            district_outages_list = ceb.get_outages()

            # Get outages for this district
            district_outages = [
                outage
                for outage in district_outages_list
                if outage.district.lower() == district.lower()
            ]

            # Extract just the outages list from the first match (if any)
            outages = district_outages[0].outages if district_outages else []

            # Return success response
            return CebOutagesByDistrictOutput(
                outages=outages,
                success=True,
            )

        except CebOutagesFailure as cf:
            # Log the error
            logging.error(f"CEB Outages error for district '{district}': {cf}")

            # Return the output
            return CebOutagesByDistrictOutput(
                outages=[],
                message=f"An error occurred while getting the CEB outages for district '{district}'. Please try again later.",
                success=False,
            )
        except Exception as e:
            # Log the error
            logging.error(
                f"Fatal error while getting ceb outages for district '{district}': {e}"
            )

            # Return the output
            return CebOutagesByDistrictOutput(
                outages=[],
                message=f"An error occurred while getting the CEB outages for district '{district}'. Please try again later.",
                success=False,
            )
