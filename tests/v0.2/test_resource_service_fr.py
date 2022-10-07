import unittest
from app import app


class TestServiceResource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        # creates a test client
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True

    def tearDown(self):
        pass

    ############################################################
    ###################### Error Handling ######################
    ############################################################

    def test_error_404(self):
        # Arrange
        url_case = [
            "/",
            "/fr",
            "/fr/service",
            "/fr/services",
        ]

        for url in url_case:
            # Act
            result = self.app.get(url)
            result_json = result.get_json()

            # Assert
            self.assertEqual(result_json["services"], [])
            self.assertEqual(
                result_json["message"],
                "No services found under this identifier. Check the docs at https://github.com/mervin16/Mauritius-Emergency-Services-Api",
            )
            self.assertFalse(result_json["success"])
            self.assertEqual(result.status_code, 404)

    ############################################################
    ###################### Resource Paths ######################
    ############################################################

    def test_services_fr_all(self):
        # Arrange
        url = "/v0.2/fr/services"
        expected_size = 18

        # Act
        result = self.app.get(url)
        result_json = result.get_json()

        # Assert
        self.assertTrue("services" in result_json)
        self.assertEqual(len(result_json["services"]), expected_size)
        self.assertEqual(result_json["message"], "")
        self.assertTrue(result_json["success"])
        self.assertEqual(result.status_code, 200)

    def test_services_sorting_asc_fr(self):
        # Arrange
        url = "/v0.2/fr/services?order=asc"
        expected_size = 18
        expected_character = "A"

        # Act
        result = self.app.get(url)
        result_json = result.get_json()
        result_character = result_json["services"][0]["name"][0]

        # Assert
        self.assertTrue("services" in result_json)
        self.assertEqual(len(result_json["services"]), expected_size)
        self.assertEqual(result_json["message"], "")
        self.assertEqual(result_character, expected_character)
        self.assertTrue(result_json["success"])
        self.assertEqual(result.status_code, 200)

    def test_services_sorting_dsc_fr(self):
        # Arrange
        url = "/v0.2/fr/services?order=dsc"
        expected_size = 18
        expected_character = "S"

        # Act
        result = self.app.get(url)
        result_json = result.get_json()
        result_character = result_json["services"][0]["name"][0]

        # Assert
        self.assertTrue("services" in result_json)
        self.assertEqual(len(result_json["services"]), expected_size)
        self.assertEqual(result_json["message"], "")
        self.assertEqual(result_character, expected_character)
        self.assertTrue(result_json["success"])
        self.assertEqual(result.status_code, 200)

    def test_services_fr_one(self):
        # Arrange
        url_case = [
            "/v0.2/fr/service/security-police-direct-2",
            "/v0.2/fr/service/health-ambulance",
            "/v0.2/fr/service/security-police-tourism",
        ]

        for url in url_case:
            # Act
            result = self.app.get(url)
            result_json = result.get_json()

            # Assert
            self.assertEqual(len(result_json["services"]), 1)
            self.assertTrue("services" in result_json)
            self.assertEqual(result_json["message"], "")
            self.assertTrue(result_json["success"])
            self.assertEqual(result.status_code, 200)

    def test_services_emergencies_only_fr(self):
        # Arrange
        url = "/v0.2/fr/services/emergencies"
        expected_size = 7

        # Act
        result = self.app.get(url)
        result_json = result.get_json()

        # Assert
        self.assertTrue("services" in result_json)
        self.assertEqual(len(result_json["services"]), expected_size)
        self.assertEqual(result_json["message"], "")
        self.assertTrue(result_json["success"])
        self.assertEqual(result.status_code, 200)

    def test_services_emergencies_only_sorting_asc_fr(self):
        # Arrange
        url = "/v0.2/fr/services/emergencies?order=asc"
        expected_size = 7
        expected_character = "A"

        # Act
        result = self.app.get(url)
        result_json = result.get_json()
        result_character = result_json["services"][0]["name"][0]

        # Assert
        self.assertTrue("services" in result_json)
        self.assertEqual(len(result_json["services"]), expected_size)
        self.assertEqual(result_json["message"], "")
        self.assertEqual(result_character, expected_character)
        self.assertTrue(result_json["success"])
        self.assertEqual(result.status_code, 200)

    def test_services_emergencies_only_sorting_dsc_fr(self):
        # Arrange
        url = "/v0.2/fr/services/emergencies?order=dsc"
        expected_size = 7
        expected_character = "S"

        # Act
        result = self.app.get(url)
        result_json = result.get_json()
        result_character = result_json["services"][0]["name"][0]

        # Assert
        self.assertTrue("services" in result_json)
        self.assertEqual(len(result_json["services"]), expected_size)
        self.assertEqual(result_json["message"], "")
        self.assertEqual(result_character, expected_character)
        self.assertTrue(result_json["success"])
        self.assertEqual(result.status_code, 200)


if __name__ == "__main__":
    unittest.main()
