from flask import Flask
from app.handlers import (
    register_error_handlers,
    register_health_check,
    register_blueprints,
)

# Create a Flask Application
app = Flask(__name__)

# Load configuration
app.config.from_prefixed_env()  # Loads FLASK_* environment variables

# Register health endpoints
register_health_check(app=app)

# Register the blueprints
register_blueprints(app=app)

# Register error handlers
register_error_handlers(app=app)
