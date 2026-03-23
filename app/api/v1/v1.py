from flask import Blueprint
from flask_restful import Api
from app.api.v1.routes.services import AllServices, OneService, EmergencyOnly
from app.api.v1.routes.cyclone import (
    CycloneReportResource,
    CycloneNamesResource,
    CycloneReportTestingResource,
    CycloneGuidelinesResource,
)
from app.api.v1.routes.ceb import CebOutages, CebOutagesByDistrict
from app.api.v1.routes.general_alerts import GeneralAlertResource
from app.api.v1.routes.alert_infos import (
    TorrentialRainPrecautionsResource,
    TorrentialRainWarningsResource,
    TsunamiPrecautionsResource,
    TsunamiWarningsResource,
)
from app.api.v1.routes.sunrise_sunset import SunriseSunsetResource
from app.api.v1.routes.moonrise_moonset import MoonriseMoonsetResource


def create_v1_blueprint(name="v1"):
    """
    Factory function to create v1 API blueprint.
    This allows creating multiple instances for different URL prefixes.
    """
    # Create the API V1 blueprint
    blueprint = Blueprint(name, __name__)

    # Generate a Flask API from the blueprint
    api = Api(blueprint)

    # > All API Routes

    # Services routes
    api.add_resource(AllServices, "/<string:lang>/services")
    api.add_resource(OneService, "/<string:lang>/service/<string:identifier>")
    api.add_resource(EmergencyOnly, "/<string:lang>/services/emergencies")

    # General alerts routes
    api.add_resource(GeneralAlertResource, "/<string:lang>/alerts")

    # Alert info routes
    api.add_resource(
        TorrentialRainPrecautionsResource,
        "/<string:lang>/alert/torrentialrain/precautions",
    )
    api.add_resource(
        TorrentialRainWarningsResource,
        "/<string:lang>/alert/torrentialrain/warnings",
    )
    api.add_resource(
        TsunamiPrecautionsResource,
        "/<string:lang>/alert/tsunami/precautions",
    )
    api.add_resource(
        TsunamiWarningsResource,
        "/<string:lang>/alert/tsunami/warnings",
    )

    # Cyclone routes
    api.add_resource(CycloneReportResource, "/<string:lang>/cyclone/report")
    api.add_resource(CycloneNamesResource, "/<string:lang>/cyclone/names")
    api.add_resource(CycloneGuidelinesResource, "/<string:lang>/cyclone/guidelines")
    api.add_resource(
        CycloneReportTestingResource, "/<string:lang>/cyclone/report/testing"
    )

    # CEB routes
    api.add_resource(CebOutages, "/<string:lang>/ceb/outages")
    api.add_resource(
        CebOutagesByDistrict, "/<string:lang>/ceb/outages/<string:district>"
    )

    # Sun routes
    api.add_resource(SunriseSunsetResource, "/<string:lang>/sun")

    # Moon routes
    api.add_resource(MoonriseMoonsetResource, "/<string:lang>/moon")

    # > Return blueprint
    return blueprint


# Create the default v1 blueprint instance
v1_blueprint = create_v1_blueprint()
