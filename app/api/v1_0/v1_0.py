from flask import Blueprint
from flask_restful import Api
import app.api.v1_0.models.services as services

# Create the API V1 blueprint
v1_0_blueprint = Blueprint("v1_0", __name__)

# Generate a Flask API from the blueprint
v1_0_api = Api(v1_0_blueprint)


# Define API Routes
v1_0_api.add_resource(services.AllServices, "/<string:lang>/services")
v1_0_api.add_resource(services.OneService, "/<string:lang>/service/<string:identifier>")
v1_0_api.add_resource(services.EmergencyOnly, "/<string:lang>/services/emergencies")