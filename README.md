Of course. I've updated the README to include a configuration section that specifies the mandatory environment variables.

-----

# Mauritius Emergency Services API

Mauritius Emergency Services is a public API that provides a list of emergency phone services in Mauritius.

## Base URL

`https://mes.mervinhemaraju.com/`

-----

## Deployment

This application is containerized using Docker and is designed for flexible deployment in different environments. It uses a single Docker image that can be configured at runtime to work with different reverse proxies like NGINX or Traefik.

### Configuration (Mandatory)

Before running the application, you must set the following mandatory environment variables. These are used for the application's mailing service.

```bash
export MAIL_USERNAME="your_email_username"
export MAIL_PASSWORD="your_email_password"
```

When using Docker Compose, you should add these variables to a `.env` file in the project's root directory.

### Flexible Startup Protocol

The Docker container uses an `entrypoint.sh` script that allows the uWSGI server to start with either the `uwsgi` or `http` protocol based on the `UWSGI_PROTOCOL` environment variable.

  - `UWSGI_PROTOCOL=uwsgi` (Default): The application listens for the binary **uwsgi** protocol. This is optimized for use with web servers like NGINX.
  - `UWSGI_PROTOCOL=http`: The application listens for the **http** protocol. This is suitable for use with ingress controllers like Traefik in a Kubernetes environment.

### 1\. Local or Web Server Deployment (with NGINX)

For local development or deployment on a web server with an NGINX proxy, you can use the included `docker-compose.yml` file.

1.  **Create a `.env` file** with the mandatory environment variables mentioned above.
2.  **Run Docker Compose**:
    ```bash
    docker-compose up --build
    ```
    This setup uses NGINX and automatically configures the application to use the `uwsgi` protocol, which is the default.

### 2\. Kubernetes Deployment (with Traefik)

When deploying to a Kubernetes cluster that uses an ingress controller like Traefik, you need to configure the application to use the `http` protocol.

In your `deployment.yaml` manifest, set the `UWSGI_PROTOCOL` environment variable to `"http"` and add the mandatory mail variables (preferably using Kubernetes Secrets).

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mes-api-deployment
# ...
spec:
  template:
    spec:
      containers:
      - name: mes-api
        image: your-image-path:latest # Replace with your image
        ports:
        - containerPort: 8081
        env:
        - name: UWSGI_PROTOCOL
          value: "http"
        # It's recommended to use secrets for sensitive data
        - name: MAIL_USERNAME
          valueFrom:
            secretKeyRef:
              name: mail-secrets
              key: username
        - name: MAIL_PASSWORD
          valueFrom:
            secretKeyRef:
              name: mail-secrets
              key: password
```

This single image can be built and pushed once, and then configured for each specific environment, ensuring consistency and simplifying the CI/CD process.

-----

## License

```
Copyright Mervin Hemaraju
```
