import pytest
import json
from app import app


class TestResourceSun:
    @pytest.fixture
    def client(self):
        # Set testing to true
        app.config["TESTING"] = True

        # Yield client
        with app.test_client() as client:
            yield client

    # > Sunrise Sunset

    testdata_sunrise_sunset = [
        ("/api/v1/en/sun"),
        ("/api/v1/fr/sun"),
    ]

    @pytest.mark.parametrize("endpoint", testdata_sunrise_sunset)
    def test_get_sunrise_sunset(self, client, endpoint):
        # Arrange

        # Act
        response = client.get(endpoint)
        result = json.loads(response.data)

        # Assert
        assert response.status_code == 200
        assert result["success"]
        assert result["message"] == ""

        assert "data" in result
        assert len(result["data"]) > 0

        first = result["data"][0]
        assert "date" in first
        assert "sunrise" in first
        assert "sunset" in first
