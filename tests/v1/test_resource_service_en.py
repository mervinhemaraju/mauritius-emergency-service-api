# import pytest
# import json
# from app import app


# class TestResourceService:
#     @pytest.fixture
#     def client(self):
#         # Set testing to true
#         app.config["TESTING"] = True

#         # Yield client
#         with app.test_client() as client:
#             yield client

#     @pytest.fixture
#     def data(self):
#         with open("data/v1/services_en.json") as services_file:
#             yield json.loads(services_file.read())

#     def test_get_all_services(self, client, data):
#         # Arrange
#         endpoint = "/api/v1/en/services"

#         # Act
#         response = client.get(endpoint)
#         result = json.loads(response.data)

#         # Assert
#         assert result["services"] == data
#         assert len(result["services"]) == len(data)
#         assert result["message"] == ""
#         assert result["success"]
