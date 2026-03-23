from bs4 import BeautifulSoup
from app.api.v1.services.moonrise_moonset import MoonriseMoonsetService


class TestServiceMoon:
    # > Moonrise Moonset

    def test_moonrise_moonset_returns_data(self):
        # Arrange
        page = open("tests/v1/dummy_data/moon/moon_1.html", "r").read()
        service = MoonriseMoonsetService.__new__(MoonriseMoonsetService)
        service.soup = BeautifulSoup(page, "html.parser")

        # Act
        result = service.get_moonrise_moonset()

        # Assert
        assert len(result) > 0

    def test_moonrise_moonset_entry_fields(self):
        # Arrange
        page = open("tests/v1/dummy_data/moon/moon_1.html", "r").read()
        service = MoonriseMoonsetService.__new__(MoonriseMoonsetService)
        service.soup = BeautifulSoup(page, "html.parser")

        # Act
        result = service.get_moonrise_moonset()
        first = result[0]

        # Assert
        assert first.date is not None
        assert hasattr(first, "phase")
        assert hasattr(first, "moonrise")
        assert hasattr(first, "moonset")

    def test_moonrise_moonset_date_format(self):
        # Arrange
        page = open("tests/v1/dummy_data/moon/moon_1.html", "r").read()
        service = MoonriseMoonsetService.__new__(MoonriseMoonsetService)
        service.soup = BeautifulSoup(page, "html.parser")

        # Act
        result = service.get_moonrise_moonset()

        # Assert — date should be in format "DD Month YYYY"
        for entry in result:
            parts = entry.date.split(" ")
            assert len(parts) == 3
            assert parts[0].isdigit()

    def test_moonrise_moonset_covers_two_months(self):
        # Arrange
        page = open("tests/v1/dummy_data/moon/moon_1.html", "r").read()
        service = MoonriseMoonsetService.__new__(MoonriseMoonsetService)
        service.soup = BeautifulSoup(page, "html.parser")

        # Act
        result = service.get_moonrise_moonset()
        months = set(entry.date.split(" ")[1] for entry in result)

        # Assert — should cover exactly 2 months
        assert len(months) == 2

    def test_moonrise_moonset_null_values_allowed(self):
        # Arrange
        page = open("tests/v1/dummy_data/moon/moon_1.html", "r").read()
        service = MoonriseMoonsetService.__new__(MoonriseMoonsetService)
        service.soup = BeautifulSoup(page, "html.parser")

        # Act
        result = service.get_moonrise_moonset()

        # Assert — some entries may have None moonrise/moonset (the "-" rows)
        # just verify the attribute exists and is either a string or None
        for entry in result:
            assert entry.moonrise is None or isinstance(entry.moonrise, str)
            assert entry.moonset is None or isinstance(entry.moonset, str)
