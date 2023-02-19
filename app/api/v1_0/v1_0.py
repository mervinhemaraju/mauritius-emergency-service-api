from flask import Blueprint
from flask_restful import Api
from app.api.v1_0.routes.services import *
from app.api.v1_0.routes.cyclone import *

# * Create the API V1 blueprint
v1_0_blueprint = Blueprint("v1_0", __name__)

# * Generate a Flask API from the blueprint
v1_0_api = Api(v1_0_blueprint)

# * Define API Routes
v1_0_api.add_resource(AllServices, "/<string:lang>/services")
v1_0_api.add_resource(OneService, "/<string:lang>/service/<string:identifier>")
v1_0_api.add_resource(EmergencyOnly, "/<string:lang>/services/emergencies")

v1_0_api.add_resource(CycloneReport, "/<string:lang>/cyclone/report")