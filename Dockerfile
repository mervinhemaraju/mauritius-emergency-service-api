# Using python 3.8 in Alpine
FROM python:3.8-alpine3.11

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Dependencies
RUN apk add python3-dev build-base linux-headers pcre-dev && pip install -r requirements.txt && apk update

# Run the command
ENTRYPOINT ["uwsgi", "app.ini"]