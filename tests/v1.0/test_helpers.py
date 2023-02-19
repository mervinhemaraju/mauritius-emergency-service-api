import pytest
from app.api.v1_0.utils.helpers import *

class TestHelper:

    testdata = [
        (
            "A cyclone warning class I is in force in Mauritius",
            "I"
        ),
        (
            "A cyclone warning class II is in force in Mauritius",
            "II"
        ),
        (
            "A cyclone warning class III is in force in Mauritius",
            "III"
        ),
        (
            "A cyclone warning class IV is in force in Mauritius",
            "IV"
        ),
        (
            "A cyclone warning class is in force in Mauritius",
            None
        ),
        (
            '''
            A cyclone warning class II is in force in Mauritius
            A cyclone warning class II is in force in Mauritius

            This is another text that is not meaningful with a class word
            ''',
            "II"
        ),
        (
            None,
            None
        ),
    ]
    @pytest.mark.parametrize("message,expected_result", testdata)
    def test_retrieve_cyclone_class_level(self,message, expected_result):

        # Act
        result = retrieve_cyclone_class_level(message)

        # Assert
        assert result == expected_result