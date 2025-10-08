#!/bin/sh
# entrypoint.sh

# Exit immediately if a command exits with a non-zero status.
set -e

# Default to the 'uwsgi' protocol if the variable is not set.
# This makes it safe for your existing NGINX setup.
PROTOCOL=${UWSGI_PROTOCOL:-uwsgi}

echo "Starting application with protocol: $PROTOCOL"

# Check the value of the environment variable
if [ "$PROTOCOL" = "http" ]; then
  # Use --http-socket for Traefik/Kubernetes on port 8081
  exec uwsgi --ini app.ini --http-socket :8081
else
  # Use --socket for NGINX on port 8000
  exec uwsgi --ini app.ini --socket :8081
fi
