import pytest
from app import app


class TestResourceError:
    @pytest.fixture
    def client(self):
        # Set testing to true
        app.config["TESTING"] = True

        # Yield client
        with app.test_client() as client:
            yield client

    testdata = [
        ("/", 302),
        ("/web", 302),
        ("/web/privacy", 200),
    ]

    @pytest.mark.parametrize("endpoint,expected_status_code", testdata)
    def test_get_report(self, client, endpoint, expected_status_code):
        # Arrange

        # Act
        response = client.get(endpoint)

        # Assert
        assert response.status_code == expected_status_code
