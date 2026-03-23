import pytest
import json
from app import app
from app.api.v1.utils.constant_others import CEB_DISTRICTS


class TestResourceCeb:
    @pytest.fixture
    def client(self):
        # Set testing to true
        app.config["TESTING"] = True

        # Yield client
        with app.test_client() as client:
            yield client

    # > All outages

    testdata_outages = [
        ("/api/v1/en/ceb/outages"),
        ("/api/v1/fr/ceb/outages"),
    ]

    @pytest.mark.parametrize("endpoint", testdata_outages)
    def test_get_all_outages(self, client, endpoint):
        # Arrange

        # Act
        response = client.get(endpoint)
        result = json.loads(response.data)

        # Assert
        assert response.status_code == 200
        assert result["success"]
        assert result["message"] == ""
        assert "district_outages" in result

    @pytest.mark.parametrize("endpoint", testdata_outages)
    def test_get_all_outages_contains_all_districts(self, client, endpoint):
        # Arrange
        expected_districts = list(CEB_DISTRICTS.values())

        # Act
        response = client.get(endpoint)
        result = json.loads(response.data)

        # Assert — all known districts should always be present in the response
        returned_districts = [d["district"] for d in result["district_outages"]]
        for district in expected_districts:
            assert district in returned_districts

    @pytest.mark.parametrize("endpoint", testdata_outages)
    def test_get_all_outages_district_structure(self, client, endpoint):
        # Arrange

        # Act
        response = client.get(endpoint)
        result = json.loads(response.data)

        # Assert — every district entry must have the expected fields
        for district_entry in result["district_outages"]:
            assert "district" in district_entry
            assert "outages" in district_entry
            assert isinstance(district_entry["outages"], list)

    @pytest.mark.parametrize("endpoint", testdata_outages)
    def test_get_all_outages_outage_structure(self, client, endpoint):
        # Arrange

        # Act
        response = client.get(endpoint)
        result = json.loads(response.data)

        # Assert — any outage present must have the expected fields
        for district_entry in result["district_outages"]:
            for outage in district_entry["outages"]:
                assert "start_datetime" in outage
                assert "end_datetime" in outage
                assert "locality" in outage
                assert "streets" in outage
                assert "_raw" in outage
                assert isinstance(outage["streets"], list)

    @pytest.mark.parametrize("endpoint", testdata_outages)
    def test_get_all_outages_raw_structure(self, client, endpoint):
        # Arrange

        # Act
        response = client.get(endpoint)
        result = json.loads(response.data)

        # Assert — _raw must have date, locality and streets
        for district_entry in result["district_outages"]:
            for outage in district_entry["outages"]:
                raw = outage["_raw"]
                assert "date" in raw
                assert "locality" in raw
                assert "streets" in raw

    # > Outages by district

    testdata_by_district = [
        (f"/api/v1/en/ceb/outages/{district}", district)
        for district in CEB_DISTRICTS.values()
    ] + [
        (f"/api/v1/fr/ceb/outages/{district}", district)
        for district in CEB_DISTRICTS.values()
    ]

    @pytest.mark.parametrize("endpoint,district", testdata_by_district)
    def test_get_outages_by_district(self, client, endpoint, district):
        # Arrange

        # Act
        response = client.get(endpoint)
        result = json.loads(response.data)

        # Assert
        assert response.status_code == 200
        assert result["success"]
        assert result["message"] == ""
        assert "outages" in result
        assert isinstance(result["outages"], list)

    @pytest.mark.parametrize("endpoint,district", testdata_by_district)
    def test_get_outages_by_district_outage_structure(self, client, endpoint, district):
        # Arrange

        # Act
        response = client.get(endpoint)
        result = json.loads(response.data)

        # Assert — any outage present must have the expected fields
        for outage in result["outages"]:
            assert "start_datetime" in outage
            assert "end_datetime" in outage
            assert "locality" in outage
            assert "streets" in outage
            assert "_raw" in outage
            assert isinstance(outage["streets"], list)

    # > Unknown district

    testdata_unknown_district = [
        ("/api/v1/en/ceb/outages/unknown-district"),
        ("/api/v1/fr/ceb/outages/unknown-district"),
    ]

    @pytest.mark.parametrize("endpoint", testdata_unknown_district)
    def test_get_outages_unknown_district_returns_empty(self, client, endpoint):
        # Arrange

        # Act
        response = client.get(endpoint)
        result = json.loads(response.data)

        # Assert — unknown district should return empty list, not an error
        assert response.status_code == 200
        assert result["success"]
        assert result["outages"] == []
