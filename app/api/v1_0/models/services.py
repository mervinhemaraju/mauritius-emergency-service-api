from flask_restful import Resource, request
import json
import app.messages.messages as MSG
import app.api.v1_0.utils.helpers as Helpers

# A list of the available json file in each language mapping its path
json_file = {
    "en": "data/v1_0/services_en.json",
    "fr": "data/v1_0/services_fr.json",
}

# The default path if language doesn't math any of them
json_def = "data/v1_0/services_en.json"

# The Service class returns a single
# item from the give parameter
class OneService(Resource):
    # GET Request
    def get(self, lang, identifier):

        # Open the file according to the language queried
        with open(json_file.get(lang, json_def)) as services_file:

            # Get the services
            services = json.load(services_file)

            # Get the queried service
            service = [
                next(filter(lambda x: x["identifier"] == identifier, services), None)
            ]

            # Checks if not empty
            if service:
                return (
                    MSG.Message.content_service(service),
                    200,
                )
            else:
                return (
                    MSG.Message.CONTENT_NOT_FOUND,
                    404,
                )


# The Services class which returns
# a list of all available services
class AllServices(Resource):
    # GET Request
    def get(self, lang):

        # Open the file according to the language queried
        with open(json_file.get(lang, json_def)) as services_file:

            # Get the services
            services = json.load(services_file)

            # Get the arguments passed
            args = request.args

            # Process services
            services = Helpers.Utils.sort_queried_service(args, services)

            # Returns the output in the correct format
            return (
                MSG.Message.content_services(services),
                200,
            )  # 200 OK HTTP VERB


# The Emergencies class returns all services with Type 'E' ONLY
# Type 'E' here means emergencies services
class EmergencyOnly(Resource):

    # GET Request
    def get(self, lang):

        # Open the file according to the language queried
        with open(json_file.get(lang, json_def)) as services_file:

            # Get the services
            services = json.load(services_file)

            # Get emergencies only
            emergencies = list(filter(lambda x: x["type"] == "E", services))

            # Get the arguments passed
            args = request.args

            # Process services
            emergencies = Helpers.Utils.sort_queried_service(args, emergencies)

            # Checks if not empty
            if emergencies:
                return (
                    MSG.Message.content_service(emergencies),
                    200,
                )
            else:
                return (
                    MSG.Message.CONTENT_NOT_FOUND,
                    404,
                )
