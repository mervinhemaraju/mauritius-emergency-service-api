import pytest
import json
from app import app
from tests.v1.constants import error_404_response


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
            error_404_response()["message"],
        ),
        (
            "/api/v1/fr/cyclone",
            error_404_response()["message"],
        ),
        (
            "/api/v1/en/service",
            error_404_response()["message"],
        ),
        (
            "/api/v1/fr/service",
            error_404_response()["message"],
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
            error_404_response()["message"],
        ),
        (
            "/api/v1/fr",
            error_404_response()["message"],
        ),
        (
            "/api/v1",
            error_404_response()["message"],
        ),
        (
            "/api/v1",
            error_404_response()["message"],
        ),
        (
            "/api",
            error_404_response()["message"],
        ),
        (
            "/api",
            error_404_response()["message"],
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
