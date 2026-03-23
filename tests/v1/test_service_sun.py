from bs4 import BeautifulSoup
from app.api.v1.services.sunrise_sunset import SunriseSunsetService


class TestServiceSun:
    # > Sunrise Sunset

    def test_sunrise_sunset_returns_data(self):
        # Arrange
        page = open("tests/v1/dummy_data/sun/sun_1.html", "r").read()
        service = SunriseSunsetService.__new__(SunriseSunsetService)
        service.soup = BeautifulSoup(page, "html.parser")

        # Act
        result = service.get_sunrise_sunset()

        # Assert
        assert len(result) > 0

    def test_sunrise_sunset_entry_fields(self):
        # Arrange
        page = open("tests/v1/dummy_data/sun/sun_1.html", "r").read()
        service = SunriseSunsetService.__new__(SunriseSunsetService)
        service.soup = BeautifulSoup(page, "html.parser")

        # Act
        result = service.get_sunrise_sunset()
        first = result[0]

        # Assert
        assert first.date is not None
        assert first.sunrise is not None
        assert first.sunset is not None

    def test_sunrise_sunset_date_format(self):
        # Arrange
        page = open("tests/v1/dummy_data/sun/sun_1.html", "r").read()
        service = SunriseSunsetService.__new__(SunriseSunsetService)
        service.soup = BeautifulSoup(page, "html.parser")

        # Act
        result = service.get_sunrise_sunset()

        # Assert — date should be in format "DD Month YYYY"
        for entry in result:
            parts = entry.date.split(" ")
            assert len(parts) == 3
            assert parts[0].isdigit()

    def test_sunrise_sunset_time_format(self):
        # Arrange
        page = open("tests/v1/dummy_data/sun/sun_1.html", "r").read()
        service = SunriseSunsetService.__new__(SunriseSunsetService)
        service.soup = BeautifulSoup(page, "html.parser")

        # Act
        result = service.get_sunrise_sunset()

        # Assert — times should be in HH:MM format
        import re

        time_pattern = re.compile(r"^\d{2}:\d{2}$")
        for entry in result:
            assert time_pattern.match(entry.sunrise)
            assert time_pattern.match(entry.sunset)

    def test_sunrise_sunset_covers_two_months(self):
        # Arrange
        page = open("tests/v1/dummy_data/sun/sun_1.html", "r").read()
        service = SunriseSunsetService.__new__(SunriseSunsetService)
        service.soup = BeautifulSoup(page, "html.parser")

        # Act
        result = service.get_sunrise_sunset()
        months = set(entry.date.split(" ")[1] for entry in result)

        # Assert — should cover exactly 2 months
        assert len(months) == 2
