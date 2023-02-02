import json
from flask_restful import Resource, request
from app.messages.messages import *
from app.api.v1_0.utils.helpers import sort_queried_service
from app.api.v1_0.utils.constants import *


# * The Service class returns a single
# * item from the give parameter
class OneService(Resource):

    # > GET Request
    def get(self, lang, identifier):

        # * Open the file according to the language queried
        with open(json_file.get(lang, json_def)) as services_file:

            # * Get the services
            services = json.load(services_file)

            # * Get the queried service
            service = [
                next(filter(lambda x: x["identifier"] == identifier, services), None)
            ]

            # * Checks if not empty
            if service:
                return (
                    content_service(service),
                    200,
                )
            else:
                return (
                    CONTENT_NOT_FOUND,
                    404,
                )


# * The Services class which returns
# * a list of all available services
class AllServices(Resource):

    # > GET Request
    def get(self, lang):

        # * Open the file according to the language queried
        with open(json_file.get(lang, json_def)) as services_file:

            # * Get the services
            services = json.load(services_file)

            # * Process services
            services = sort_queried_service(request.args, services)

            # * Returns the output in the correct format
            return (
                content_services(services),
                200,
            )  # * 200 OK HTTP VERB


# * The Emergencies class returns all services with Type 'E' ONLY
# * Type 'E' here means emergencies services
class EmergencyOnly(Resource):

    # > GET Request
    def get(self, lang):

        # * Open the file according to the language queried
        with open(json_file.get(lang, json_def)) as services_file:

            # * Get the services
            services = json.load(services_file)

            # * Get emergencies only
            emergencies = list(filter(lambda x: x["type"] == "E", services))

            # * Process services
            emergencies = sort_queried_service(request.args, emergencies)

            # * Checks if not empty
            if emergencies:
                return (
                    content_service(emergencies),
                    200,
                )
            else:
                return (
                    CONTENT_NOT_FOUND,
                    404,
                )
