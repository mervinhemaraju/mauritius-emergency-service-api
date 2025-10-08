# Use the python 3.11.10 alpine image
FROM python:3.11.10-alpine3.19

# Set the working directory to /app
WORKDIR /app

# Install system dependencies for uWSGI (do this before copying application code)
# Combine apk commands and clean up cache to reduce image size
RUN apk add --no-cache --virtual .build-deps \
    python3-dev \
    build-base \
    linux-headers \
    pcre-dev \
    && apk add --no-cache pcre

# Copy only requirements first to leverage Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Remove build dependencies to reduce image size
RUN apk del .build-deps

# Copy and make the entrypoint script executable
COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh

# Create a non-root user
RUN adduser -D th3pl4gu3

# Copy application code (done after pip install for better caching)
COPY --chown=th3pl4gu3:th3pl4gu3 . /app

# Switch to non-root user
USER th3pl4gu3

# * Run the entrypoint script
ENTRYPOINT ["/entrypoint.sh"]