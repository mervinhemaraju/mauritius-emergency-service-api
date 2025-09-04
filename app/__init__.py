import os
import app.web.web as Web
from app.api.v1.v1 import v1_blueprint
from app.api.v1.models.errors import Error
from flask import Flask, redirect, url_for
from flask_restful import marshal_with

# * Create a Flask Application
app = Flask(__name__)

# * Register Blueprints
# > API Blueprint
app.register_blueprint(v1_blueprint, url_prefix="/api/v1")

# > Web App Blueprints
app.register_blueprint(Web.web, url_prefix="/web")

# * SMTP Settings
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USERNAME"] = os.environ["MAIL_USERNAME"]
app.config["MAIL_PASSWORD"] = os.environ["MAIL_PASSWORD"]
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False


# * Redirect to the correct web page by default
@app.route("/")
@app.route("/web")
def page_web():
    return redirect(url_for("web.home_view"))


# * Health Check Endpoint
@app.route("/health")
@app.route("/web/health")
def page_health():
    return {"status": "ok"}, 200


#! Error Handlers
@app.errorhandler(404)  #! Handling HTTP 404 NOT FOUND
@marshal_with(Error.error_fields)
def page_not_found(e):
    # * Create a new error object and return it
    return Error(
        message="You've landed on a non-existant page. Please check our docs at https://github.com/mervinhemaraju/mauritius-emergency-service-api",
        code=404,
    ), 404


@app.errorhandler(400)  #! Handling HTTP 400 BAD REQUEST
@marshal_with(Error.error_fields)
def page_bad_request(e):
    # * Create a new error object and return it
    return Error(
        message="You've sent a bad request. Please check our docs at https://github.com/mervinhemaraju/mauritius-emergency-service-api",
        code=400,
    ), 400
