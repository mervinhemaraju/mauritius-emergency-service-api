from flask import Blueprint
from flask_restful import Api
from app.api.v1.routes.services import AllServices, OneService, EmergencyOnly
from app.api.v1.routes.cyclone import CycloneReportResource, CycloneNamesResource

# * Create the API V1 blueprint
v1_blueprint = Blueprint("v1", __name__)

# * Generate a Flask API from the blueprint
v1_api = Api(v1_blueprint)

# * Define API Routes
v1_api.add_resource(AllServices, "/<string:lang>/services")
v1_api.add_resource(OneService, "/<string:lang>/service/<string:identifier>")
v1_api.add_resource(EmergencyOnly, "/<string:lang>/services/emergencies")

v1_api.add_resource(CycloneReportResource, "/<string:lang>/cyclone/report")
v1_api.add_resource(CycloneNamesResource, "/<string:lang>/cyclone/names")
# v1_api.add_resource(CycloneTest, "/<string:lang>/cyclone/test")
