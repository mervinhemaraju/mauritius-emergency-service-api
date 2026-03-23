import pytest
import json
from app import app


class TestResourceTides:
    @pytest.fixture
    def client(self):
        # Set testing to true
        app.config["TESTING"] = True

        # Yield client
        with app.test_client() as client:
            yield client

    # > Tides

    testdata_tides = [
        ("/api/v1/en/tides"),
        ("/api/v1/fr/tides"),
    ]

    @pytest.mark.parametrize("endpoint", testdata_tides)
    def test_get_tides(self, client, endpoint):
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
        assert "high_tide_1" in first
        assert "high_tide_2" in first
        assert "low_tide_1" in first
        assert "low_tide_2" in first
