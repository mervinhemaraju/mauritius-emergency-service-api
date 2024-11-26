import pytest
import json
from app import app


class TestResourceError:
    @pytest.fixture
    def client(self):
        # Set testing to true
        app.config["TESTING"] = True

        # Yield client
        with app.test_client() as client:
            yield client

    testdata = [
        (
            "/api/v1/en/cyclone",
            "You've landed on a non-existant page. Please check our docs at https://github.com/mervinhemaraju/mauritius-emergency-service-api",
        ),
        (
            "/api/v1/fr/cyclone",
            "You've landed on a non-existant page. Please check our docs at https://github.com/mervinhemaraju/mauritius-emergency-service-api",
        ),
        (
            "/api/v1/en/service",
            "You've landed on a non-existant page. Please check our docs at https://github.com/mervinhemaraju/mauritius-emergency-service-api",
        ),
        (
            "/api/v1/fr/service",
            "You've landed on a non-existant page. Please check our docs at https://github.com/mervinhemaraju/mauritius-emergency-service-api",
        ),
        (
            "/api/v1/en/service/unknown",
            "The service 'unknown' cannot be found.",
        ),
        (
            "/api/v1/fr/service/unknown",
            "The service 'unknown' cannot be found.",
        ),
        (
            "/api/v1/en",
            "You've landed on a non-existant page. Please check our docs at https://github.com/mervinhemaraju/mauritius-emergency-service-api",
        ),
        (
            "/api/v1/fr",
            "You've landed on a non-existant page. Please check our docs at https://github.com/mervinhemaraju/mauritius-emergency-service-api",
        ),
        (
            "/api/v1",
            "You've landed on a non-existant page. Please check our docs at https://github.com/mervinhemaraju/mauritius-emergency-service-api",
        ),
        (
            "/api/v1",
            "You've landed on a non-existant page. Please check our docs at https://github.com/mervinhemaraju/mauritius-emergency-service-api",
        ),
        (
            "/api",
            "You've landed on a non-existant page. Please check our docs at https://github.com/mervinhemaraju/mauritius-emergency-service-api",
        ),
        (
            "/api",
            "You've landed on a non-existant page. Please check our docs at https://github.com/mervinhemaraju/mauritius-emergency-service-api",
        ),
    ]

    @pytest.mark.parametrize("endpoint,error_message", testdata)
    def test_get_report(self, client, endpoint, error_message):
        # Arrange

        # Act
        response = client.get(endpoint)
        result = json.loads(response.data)

        # Assert
        assert result["message"] == error_message
        assert not result["success"]
        assert response.status_code == 404
