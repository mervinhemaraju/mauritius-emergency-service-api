import pytest
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
        ("/health", {"status": "ok"}, 200),
        ("/web/health", {"status": "ok"}, 200),
        ("/api/v1/health", {"status": "ok"}, 200),
        (
            "/api/health",
            error_404_response(),
            404,
        ),
    ]

    @pytest.mark.parametrize("endpoint,expected_payload,expected_status_code", testdata)
    def test_get_report(self, client, endpoint, expected_payload, expected_status_code):
        # Arrange

        # Act
        response = client.get(endpoint)

        # Assert
        assert response.status_code == expected_status_code
        assert response.json == expected_payload
