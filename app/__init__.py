from flask import Flask, redirect,url_for
import app.api.v0_2.v0_2 as V0_2
import app.api.v1_0.v1_0 as V1_0
import app.web.web as Web
import app.messages.messages as MSG
import os

# Create a Flask Application
app = Flask(__name__)

# Register Blueprints
app.register_blueprint(V0_2.v0_2_blueprint, url_prefix="/api/v0.2")
app.register_blueprint(V1_0.v1_0_blueprint, url_prefix="/api/v1")
app.register_blueprint(Web.web, url_prefix="/web")

# SMTP Settings
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USERNAME"] = os.environ["MAIL_USERNAME"]
app.config["MAIL_PASSWORD"] = os.environ["MAIL_PASSWORD"]
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False

# Redirect to the correct web page by default
@app.route("/")
@app.route("/web")
def page_web():
    return redirect(url_for("web.home_view"))

# Error Handlers
@app.errorhandler(404)  # Handling HTTP 404 NOT FOUND
def page_not_found(e):
    return (
        MSG.Message.CONTENT_NOT_FOUND,
        404,
    )


@app.errorhandler(400)  # Handling HTTP 400 BAD REQUEST
def page_bad_request(e):
    return (
        MSG.Message.CONTENT_BAD_REQUEST,
        400,
    )

