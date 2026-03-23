from bs4 import BeautifulSoup
from app.api.v1.services.tides import TidesService


class TestServiceTides:
    # > Tides

    def test_tides_returns_data(self):
        # Arrange
        page = open("tests/v1/dummy_data/tides/tides_1.html", "r").read()
        service = TidesService.__new__(TidesService)
        service.soup = BeautifulSoup(page, "html.parser")

        # Act
        result = service.get_tides()

        # Assert
        assert len(result) > 0

    def test_tides_entry_fields(self):
        # Arrange
        page = open("tests/v1/dummy_data/tides/tides_1.html", "r").read()
        service = TidesService.__new__(TidesService)
        service.soup = BeautifulSoup(page, "html.parser")

        # Act
        result = service.get_tides()
        first = result[0]

        # Assert
        assert first.date is not None
        assert hasattr(first, "high_tide_1")
        assert hasattr(first, "high_tide_2")
        assert hasattr(first, "low_tide_1")
        assert hasattr(first, "low_tide_2")

    def test_tides_date_format(self):
        # Arrange
        page = open("tests/v1/dummy_data/tides/tides_1.html", "r").read()
        service = TidesService.__new__(TidesService)
        service.soup = BeautifulSoup(page, "html.parser")

        # Act
        result = service.get_tides()

        # Assert — date should be in format "DD Month YYYY"
        for entry in result:
            parts = entry.date.split(" ")
            assert len(parts) == 3
            assert parts[0].isdigit()

    def test_tides_covers_two_months(self):
        # Arrange
        page = open("tests/v1/dummy_data/tides/tides_1.html", "r").read()
        service = TidesService.__new__(TidesService)
        service.soup = BeautifulSoup(page, "html.parser")

        # Act
        result = service.get_tides()
        months = set(entry.date.split(" ")[1] for entry in result)

        # Assert — should cover exactly 2 months
        assert len(months) == 2

    def test_tides_null_values_allowed(self):
        # Arrange
        page = open("tests/v1/dummy_data/tides/tides_1.html", "r").read()
        service = TidesService.__new__(TidesService)
        service.soup = BeautifulSoup(page, "html.parser")

        # Act
        result = service.get_tides()

        # Assert — tide entries may be None on irregular tide days
        for entry in result:
            assert entry.high_tide_1 is None or hasattr(entry.high_tide_1, "time")
            assert entry.high_tide_2 is None or hasattr(entry.high_tide_2, "time")
            assert entry.low_tide_1 is None or hasattr(entry.low_tide_1, "time")
            assert entry.low_tide_2 is None or hasattr(entry.low_tide_2, "time")

    def test_tides_tide_entry_has_time_and_height(self):
        # Arrange
        page = open("tests/v1/dummy_data/tides/tides_1.html", "r").read()
        service = TidesService.__new__(TidesService)
        service.soup = BeautifulSoup(page, "html.parser")

        # Act
        result = service.get_tides()

        # Assert — any non-null tide should have both time and height_cm
        for entry in result:
            for tide in [
                entry.high_tide_1,
                entry.high_tide_2,
                entry.low_tide_1,
                entry.low_tide_2,
            ]:
                if tide is not None:
                    assert tide.time is not None
                    assert tide.height_cm is not None
