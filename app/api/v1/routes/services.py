from flask_restful import Resource, request, marshal_with
from app.api.v1.services.service import Services
from app.api.v1.models.services import ServicesOutput
from app.api.v1.utils.helpers import sort_queried_service


# * The Service class returns a single
# * item from the give parameter
class OneService(Resource):
    # > GET Request
    @marshal_with(ServicesOutput.service_output_fields)
    def get(self, lang, identifier):
        # * Create a new output object
        output = ServicesOutput()

        # * Retrieve the services
        services = Services(lang).load()

        # * Get the queried service
        service = next(filter(lambda x: x.identifier == identifier, services), None)

        # * Check if service is found
        if service:
            # * Update the output object
            output.services = [service]
            output.success = True

            # * Return the output
            return output, 200
        else:
            # * Update the output
            output.services = []
            output.success = False
            output.message = f"The service '{identifier}' cannot be found."

            # * Return the output
            return output, 404


# * The Services class which returns
# * a list of all available services
class AllServices(Resource):
    # > GET Request
    @marshal_with(ServicesOutput.service_output_fields)
    def get(self, lang):
        # * Retrieve the services
        services = Services(lang).load()

        # * Process services
        services = sort_queried_service(request.args, services)

        # * Create a services output object
        output = ServicesOutput(services=services, success=True)

        # * Returns the output in the correct format
        return output, 200


# * The Emergencies class returns all services with Type 'E' ONLY
# * Type 'E' here means emergencies services
class EmergencyOnly(Resource):
    # > GET Request
    @marshal_with(ServicesOutput.service_output_fields)
    def get(self, lang):
        # * Retrieve the services
        services = Services(lang).load()

        # * Get emergencies only
        emergencies = list(filter(lambda x: x.type == "E", services))

        # * Process services
        emergencies = sort_queried_service(request.args, emergencies)

        # * Create an output servcice object
        output = ServicesOutput(services=emergencies, success=True)

        # * Return the output
        return output, 202
