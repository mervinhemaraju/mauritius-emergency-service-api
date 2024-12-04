import pytest
import json
import re
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

        assert result["report"]["level"] in [0, 1, 2, 3, 4]

        if result["report"]["level"] > 0:
            time_pattern = re.compile(r"^\d{2}:\d{2}:\d{2}$")
            assert time_pattern.match(result["report"]["next_bulletin"])

        assert result["message"] == ""
        assert result["success"]
        assert response.status_code == 200

    testdata = [
        ("/api/v1/en/cyclone/report/testing"),
        ("/api/v1/fr/cyclone/report/testing"),
    ]

    @pytest.mark.parametrize("endpoint", testdata)
    def test_get_report_testing(self, client, endpoint):
        # Arrange

        # Act
        response = client.get(endpoint)
        result = json.loads(response.data)

        # Assertions

        # * Assert presence on fields
        assert "report" in result
        assert "level" in result["report"]
        assert "news" in result["report"]
        assert "next_bulletin" in result["report"]

        # * Assert validity of fields
        assert result["report"]["level"] in [0, 1, 2, 3, 4]

        if result["report"]["level"] > 0:
            time_pattern = re.compile(r"^\d{2}:\d{2}:\d{2}$")
            assert time_pattern.match(result["report"]["next_bulletin"])

        assert result["message"] == ""
        assert result["success"]
        assert response.status_code == 200

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
        assert "name" in result["names"][0]
        assert "gender" in result["names"][0]
        assert "named_by" in result["names"][0]
        assert "provided_by" in result["names"][0]
        assert result["message"] == ""
        assert result["success"]
        assert response.status_code == 200

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
        assert "level" in result["guidelines"][0]
        assert "description" in result["guidelines"][0]
        assert "precautions" in result["guidelines"][0]
        assert result["message"] == ""
        assert result["success"]
        assert response.status_code == 200
