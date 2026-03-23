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
from app.api.v1.routes.rainfall import HeavyRainfallAlertsResource


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

    # Heavy Rainfall Alerts
    api.add_resource(HeavyRainfallAlertsResource, "/<string:lang>/hra")

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

    # > Return blueprint
    return blueprint


# Create the default v1 blueprint instance
v1_blueprint = create_v1_blueprint()
