import pytest
import json
from app import app


class TestResourceMoon:
    @pytest.fixture
    def client(self):
        # Set testing to true
        app.config["TESTING"] = True

        # Yield client
        with app.test_client() as client:
            yield client

    # > Moonrise Moonset
    testdata_moonrise_moonset = [
        ("/api/v1/en/moon"),
        ("/api/v1/fr/moon"),
    ]

    @pytest.mark.parametrize("endpoint", testdata_moonrise_moonset)
    def test_get_moonrise_moonset(self, client, endpoint):
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
        assert "phase" in first
        assert "moonrise" in first
        assert "moonset" in first
