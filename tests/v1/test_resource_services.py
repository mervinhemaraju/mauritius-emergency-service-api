import pytest
import json
from app import app


class TestResourceService:
    def one_service(lang: str, identifier: str):
        with open(f"data/v1/services_{lang}.json") as services_file:
            services = json.loads(services_file.read())
            return [
                service for service in services if service["identifier"] == identifier
            ]

    def get_services(lang: str):
        with open(f"data/v1/services_{lang}.json") as services_file:
            return json.loads(services_file.read())

    def get_emergencies(lang: str):
        with open(f"data/v1/services_{lang}.json") as services_file:
            services = json.loads(services_file.read())
            return [service for service in services if service["type"] == "E"]

    @pytest.fixture
    def client(self):
        # Set testing to true
        app.config["TESTING"] = True

        # Yield client
        with app.test_client() as client:
            yield client

    testdata = [
        ("/api/v1/en/services", list(get_services(lang="en"))),
        ("/api/v1/en/services/emergencies", list(get_emergencies(lang="en"))),
        ("/api/v1/fr/services", list(get_services(lang="fr"))),
        ("/api/v1/fr/services/emergencies", list(get_emergencies(lang="fr"))),
        (
            "/api/v1/en/service/security-police-direct",
            list(one_service(lang="en", identifier="security-police-direct")),
        ),
        (
            "/api/v1/fr/service/security-police-direct",
            list(one_service(lang="fr", identifier="security-police-direct")),
        ),
    ]

    @pytest.mark.parametrize("endpoint,expected_result", testdata)
    def test_get_all_services(self, client, endpoint, expected_result):
        # Arrange

        # Act
        response = client.get(endpoint)
        result = json.loads(response.data)

        # Assert
        assert result["services"] == expected_result
        assert len(result["services"]) == len(expected_result)
        assert result["message"] == ""
        assert result["success"]
        assert response.status_code == 200
