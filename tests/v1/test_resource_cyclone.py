import pytest
import json
from app import app


class TestResourceCyclone:
    @pytest.fixture
    def client(self):
        # Set testing to true
        app.config["TESTING"] = True

        # Yield client
        with app.test_client() as client:
            yield client

    testdata = [
        ("/api/v1/en/cyclone/report"),
        ("/api/v1/fr/cyclone/report"),
    ]

    @pytest.mark.parametrize("endpoint", testdata)
    def test_get_report(self, client, endpoint):
        # Arrange

        # Act
        response = client.get(endpoint)
        result = json.loads(response.data)

        # Assert
        assert "report" in result
        assert "level" in result["report"]
        assert "news" in result["report"]
        assert "next_bulletin" in result["report"]
        assert result["message"] == ""
        assert result["success"]

    testdata = [
        ("/api/v1/en/cyclone/names"),
        ("/api/v1/fr/cyclone/names"),
    ]

    @pytest.mark.parametrize("endpoint", testdata)
    def test_get_names(self, client, endpoint):
        # Arrange

        # Act
        response = client.get(endpoint)
        result = json.loads(response.data)

        # Assert
        assert "names" in result
        assert len(result["names"]) > 0
        assert result["message"] == ""
        assert result["success"]

    testdata = [
        ("/api/v1/en/cyclone/guidelines"),
        ("/api/v1/fr/cyclone/guidelines"),
    ]

    @pytest.mark.parametrize("endpoint", testdata)
    def test_get_guidelines(self, client, endpoint):
        # Arrange

        # Act
        response = client.get(endpoint)
        result = json.loads(response.data)

        # Assert
        assert "guidelines" in result
        assert len(result["guidelines"]) > 0
        assert result["message"] == ""
        assert result["success"]
