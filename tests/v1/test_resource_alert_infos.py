import pytest
import json
from app import app


class TestResourceAlertInfos:
    @pytest.fixture
    def client(self):
        # Set testing to true
        app.config["TESTING"] = True

        # Yield client
        with app.test_client() as client:
            yield client

    # > Torrential Rain Precautions

    testdata_torrential_rain_precautions = [
        ("/api/v1/en/alert/torrentialrain/precautions"),
        ("/api/v1/fr/alert/torrentialrain/precautions"),
    ]

    @pytest.mark.parametrize("endpoint", testdata_torrential_rain_precautions)
    def test_get_torrential_rain_precautions(self, client, endpoint):
        # Arrange

        # Act
        response = client.get(endpoint)
        result = json.loads(response.data)

        # Assert
        assert response.status_code == 200
        assert result["success"]
        assert result["message"] == ""

        assert "data" in result
        assert "id" in result["data"]
        assert "title" in result["data"]
        assert "sections" in result["data"]

        assert result["data"]["id"] == "torrential_rain_precautions"
        assert len(result["data"]["sections"]) > 0

        first_section = result["data"]["sections"][0]
        assert "id" in first_section
        assert "title" in first_section

    # > Torrential Rain Warnings

    testdata_torrential_rain_warnings = [
        ("/api/v1/en/alert/torrentialrain/warnings"),
        ("/api/v1/fr/alert/torrentialrain/warnings"),
    ]

    @pytest.mark.parametrize("endpoint", testdata_torrential_rain_warnings)
    def test_get_torrential_rain_warnings(self, client, endpoint):
        # Arrange

        # Act
        response = client.get(endpoint)
        result = json.loads(response.data)

        # Assert
        assert response.status_code == 200
        assert result["success"]
        assert result["message"] == ""

        assert "data" in result
        assert "id" in result["data"]
        assert "title" in result["data"]
        assert "sections" in result["data"]

        assert result["data"]["id"] == "torrential_rain_warning_system"
        assert len(result["data"]["sections"]) > 0

        first_section = result["data"]["sections"][0]
        assert "id" in first_section
        assert "title" in first_section
        assert "content" in first_section

        # * The warning bulletin section should have stakeholders
        warning_bulletin = next(
            (s for s in result["data"]["sections"] if s["id"] == "warning_bulletin"),
            None,
        )
        assert warning_bulletin is not None
        assert "stakeholders" in warning_bulletin
        assert len(warning_bulletin["stakeholders"]) > 0

    # > Tsunami Precautions

    testdata_tsunami_precautions = [
        ("/api/v1/en/alert/tsunami/precautions"),
        ("/api/v1/fr/alert/tsunami/precautions"),
    ]

    @pytest.mark.parametrize("endpoint", testdata_tsunami_precautions)
    def test_get_tsunami_precautions(self, client, endpoint):
        # Arrange

        # Act
        response = client.get(endpoint)
        result = json.loads(response.data)

        # Assert
        assert response.status_code == 200
        assert result["success"]
        assert result["message"] == ""

        assert "data" in result
        assert "id" in result["data"]
        assert "title" in result["data"]
        assert "sections" in result["data"]

        assert result["data"]["id"] == "tsunami_precautions"
        assert len(result["data"]["sections"]) > 0

        # * The things_to_remember section should have a precautions list
        things_to_remember = next(
            (s for s in result["data"]["sections"] if s["id"] == "things_to_remember"),
            None,
        )
        assert things_to_remember is not None
        assert "precautions" in things_to_remember
        assert len(things_to_remember["precautions"]) > 0

    # > Tsunami Warnings

    testdata_tsunami_warnings = [
        ("/api/v1/en/alert/tsunami/warnings"),
        ("/api/v1/fr/alert/tsunami/warnings"),
    ]

    @pytest.mark.parametrize("endpoint", testdata_tsunami_warnings)
    def test_get_tsunami_warnings(self, client, endpoint):
        # Arrange

        # Act
        response = client.get(endpoint)
        result = json.loads(response.data)

        # Assert
        assert response.status_code == 200
        assert result["success"]
        assert result["message"] == ""

        assert "data" in result
        assert "id" in result["data"]
        assert "title" in result["data"]
        assert "sections" in result["data"]

        assert result["data"]["id"] == "tsunami_warning_system"
        assert len(result["data"]["sections"]) > 0

        # * The warning_system section should have stages
        warning_system = next(
            (s for s in result["data"]["sections"] if s["id"] == "warning_system"),
            None,
        )
        assert warning_system is not None
        assert "stages" in warning_system
        assert len(warning_system["stages"]) == 3

        # * Each stage should have the expected fields
        for stage in warning_system["stages"]:
            assert "id" in stage
            assert "level" in stage
            assert "title" in stage
            assert "content" in stage

        # * Assert stage levels are 1, 2, 3 in order
        levels = [s["level"] for s in warning_system["stages"]]
        assert levels == [1, 2, 3]

    # > Invalid language fallback — should still return data (defaults to english)

    testdata_invalid_lang = [
        ("/api/v1/de/alert/torrentialrain/precautions"),
        ("/api/v1/de/alert/torrentialrain/warnings"),
        ("/api/v1/de/alert/tsunami/precautions"),
        ("/api/v1/de/alert/tsunami/warnings"),
    ]

    @pytest.mark.parametrize("endpoint", testdata_invalid_lang)
    def test_invalid_lang_falls_back_to_default(self, client, endpoint):
        # Arrange

        # Act
        response = client.get(endpoint)
        result = json.loads(response.data)

        # Assert — should fall back to default language, not crash
        assert response.status_code == 200
        assert result["success"]
        assert "data" in result
        assert result["data"] is not None
