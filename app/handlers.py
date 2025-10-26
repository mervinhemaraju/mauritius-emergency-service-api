from flask_restful import marshal_with
from app.api.v1.models.errors import Error
from app.api.v1.v1 import v1_blueprint, create_v1_blueprint


def register_error_handlers(app):
    """
    Register custom error handlers.
    """

    @app.errorhandler(404)
    @marshal_with(Error.error_fields)
    def handle_not_found(e):
        return Error(
            message="You've landed on a non-existant endpoint. Please check our docs at https://github.com/mervinhemaraju/mauritius-emergency-service-api",
            code=404,
        ), 404

    @app.errorhandler(400)
    @marshal_with(Error.error_fields)
    def handle_bad_request(e):
        return Error(
            message="You've sent an invalid request. See documentation: https://github.com/mervinhemaraju/mauritius-emergency-service-api",
            code=400,
        ), 400

    @app.errorhandler(500)
    @marshal_with(Error.error_fields)
    def handle_internal_error(e):
        return Error(
            message="An internal server error occurred. Please try again later.",
            code=500,
        ), 500


def register_blueprints(app):
    """
    Register all application blueprints.
    """
    # Primary URL pattern
    app.register_blueprint(v1_blueprint, url_prefix="/v1")
    # Legacy URL pattern - create a second blueprint instance
    v1_legacy_blueprint = create_v1_blueprint(name="v1_legacy")
    app.register_blueprint(v1_legacy_blueprint, url_prefix="/api/v1")


def register_health_check(app):
    """
    Register health check endpoint.
    """

    @app.route("/health")
    def health_check():
        return {"status": "ok"}, 200
