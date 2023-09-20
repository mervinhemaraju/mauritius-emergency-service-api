import pytest
from bs4 import BeautifulSoup
from app.api.v1_0.models.cyclone import Cyclone
from app.api.v1_0.models.exceptions import CycloneReportFailure

class TestCyclone:

    testdata = [
        (
            "tests/v1.0/dummy_data/cyclone_class_1.html",
            "23:00:00"
        ),
        (
            "tests/v1.0/dummy_data/cyclone_class_2.html",
            "22:10:00"
        ),
        (
            "tests/v1.0/dummy_data/cyclone_class_3.html",
            "12:10:00"
        ),
        (
            "tests/v1.0/dummy_data/cyclone_class_4.html",
            "22:10:00"
        ),
        (
            "tests/v1.0/dummy_data/cyclone_class_none.html",
            None
        ),
    ]
    @pytest.mark.parametrize("file,expected_result", testdata)
    def test_get_next_bulletin(self,file, expected_result):

        # Act
        page = open(file, 'r').read()

        cyclone = Cyclone()
        cyclone.soup = BeautifulSoup(page, 'html.parser')
        result = cyclone.next_bulletin()

        # Assert
        assert result == expected_result

    testdata = [
        (
            "tests/v1.0/dummy_data/cyclone_class_1.html",
            1
        ),
        (
            "tests/v1.0/dummy_data/cyclone_class_2.html",
            2
        ),
        (
            "tests/v1.0/dummy_data/cyclone_class_3.html",
            3
        ),
        (
            "tests/v1.0/dummy_data/cyclone_class_4.html",
            4
        ),
        (
            "tests/v1.0/dummy_data/cyclone_class_none.html",
            "Could not retrieve cyclone level."
        ),
    ]
    @pytest.mark.parametrize("file,expected_result", testdata)
    def test_get_class_level(self,file, expected_result):

        # Act
        try:

            page = open(file, 'r').read()

            cyclone = Cyclone()
            cyclone.soup = BeautifulSoup(page, 'html.parser')
            result = cyclone.class_level()
        except CycloneReportFailure as e:
            result = str(e)

        # Assert
        assert result == expected_result
