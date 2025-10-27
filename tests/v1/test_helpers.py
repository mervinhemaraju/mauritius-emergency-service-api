import pytest
from datetime import datetime
from app.api.v1.utils.helpers import (
    retrieve_cyclone_class_level,
    retrieve_time_from_text,
    parse_ceb_datetimes,
    retrieve_ceb_streets,
)


class TestHelper:
    testdata = [
        (
            "Le dimanche 26 octobre 2025 de 08:30:00 à 14:00:00",
            datetime(day=26, month=10, year=2025, hour=8, minute=30, second=0),
            datetime(day=26, month=10, year=2025, hour=14, minute=0, second=0),
        ),
        (
            "le dimanche 26 octobre 2025 de  08:30:00 à  16:00:00",
            datetime(day=26, month=10, year=2025, hour=8, minute=30, second=0),
            datetime(day=26, month=10, year=2025, hour=16, minute=0, second=0),
        ),
        (
            "LE jeudi 30 octobre 2025 de  08:30:00 à  17:00:00",
            datetime(day=30, month=10, year=2025, hour=8, minute=30, second=0),
            datetime(day=30, month=10, year=2025, hour=17, minute=0, second=0),
        ),
        (
            "Le mercredi 12 january 2026 de  18:30:30 à  23:20:00",
            datetime(day=12, month=1, year=2026, hour=18, minute=30, second=30),
            datetime(day=12, month=1, year=2026, hour=23, minute=20, second=0),
        ),
        (
            "Le mercredi 12 aout 2026 de  18:30:30 à  23:20:00",
            datetime(day=12, month=8, year=2026, hour=18, minute=30, second=30),
            datetime(day=12, month=8, year=2026, hour=23, minute=20, second=0),
        ),
        (
            "Le mercredi 12 august 2026 de  18:30:30 à  23:20:00",
            datetime(day=12, month=8, year=2026, hour=18, minute=30, second=30),
            datetime(day=12, month=8, year=2026, hour=23, minute=20, second=0),
        ),
        (
            "Le mercredi 12 août 2026 de  18:30:30 à  23:20:00",
            datetime(day=12, month=8, year=2026, hour=18, minute=30, second=30),
            datetime(day=12, month=8, year=2026, hour=23, minute=20, second=0),
        ),
        (
            "Le mercredi 12 février 2026 de  18:30:30 à  23:20:00",
            datetime(day=12, month=2, year=2026, hour=18, minute=30, second=30),
            datetime(day=12, month=2, year=2026, hour=23, minute=20, second=0),
        ),
        (
            "Le mercredi 12 fevrier 2026 de  18:30:30 à  23:20:00",
            datetime(day=12, month=2, year=2026, hour=18, minute=30, second=30),
            datetime(day=12, month=2, year=2026, hour=23, minute=20, second=0),
        ),
        (
            "Le mercredi 12 february 2026 de  18:30:30 à  23:20:00",
            datetime(day=12, month=2, year=2026, hour=18, minute=30, second=30),
            datetime(day=12, month=2, year=2026, hour=23, minute=20, second=0),
        ),
        (
            "Le mercredi 12 february 2026 de  18:30:30 à 23:20:00",
            datetime(day=12, month=2, year=2026, hour=18, minute=30, second=30),
            datetime(day=12, month=2, year=2026, hour=23, minute=20, second=0),
        ),
        # Non working tests
        ("mercredi 12 february 2026 de  18:30:30 à  23:20:00", None, None),
        ("Le mercredi 12 autubre 2026 de  18:30:30 à  23:20:00", None, None),
        ("Le mercredi 12 february 2026 de  18:30:30  23:20:00", None, None),
    ]

    @pytest.mark.parametrize(
        "date_string,expected_start_datetime,expected_end_datetime", testdata
    )
    def test_parse_ceb_datetimes(
        self, date_string, expected_start_datetime, expected_end_datetime
    ):
        # Act
        result_start_datetime, result_end_datetime = parse_ceb_datetimes(
            date_string=date_string
        )

        # Assert
        assert result_start_datetime == expected_start_datetime
        assert result_end_datetime == expected_end_datetime

    testdata = [
        ("A cyclone warning class I is in force in Mauritius", "I"),
        ("A cyclone warning class II is in force in Mauritius", "II"),
        ("A cyclone warning class III is in force in Mauritius", "III"),
        ("A cyclone warning class IV is in force in Mauritius", "IV"),
        ("A cyclone warning class is in force in Mauritius", None),
        (
            """
            A cyclone warning class II is in force in Mauritius
            A cyclone warning class II is in force in Mauritius

            This is another text that is not meaningful with a class word
            """,
            "II",
        ),
        (None, None),
    ]

    @pytest.mark.parametrize("message,expected_result", testdata)
    def test_retrieve_cyclone_class_level(self, message, expected_result):
        # Act
        result = retrieve_cyclone_class_level(message, keyword="class")

        # Assert
        assert result == expected_result

    testdata = [
        ("The next bulletin will be issued at around 23h00.", "23:00:00"),
        ("The next bulletin will be issued at around 22h10.", "22:10:00"),
        ("The next bulletin will be issued at around 12h10.", "12:10:00"),
        ("The next bulletin will be issued at around 12:05.", "12:05:00"),
        ("The next bulletin will be issued at around nine.", None),
        (None, None),
    ]

    @pytest.mark.parametrize("message,expected_result", testdata)
    def test_retrieve_time_from_text(self, message, expected_result):
        # Act
        result = retrieve_time_from_text(message)

        # Assert
        assert result == expected_result

    testdata = [
        (
            "MORC BARACHOIS TAMARIN, PALM BAY ET VILLA TAMARIN",
            ["morc barachois tamarin", "palm bay", "villa tamarin"],
        ),
        (
            "dans les périmètres de La Lucie Roy, Morc Lotus, NSLD Bel Air, Morc Le Florent, Route Royale Ernest Florent et Chemin Gandhi",
            [
                "dans les périmètres de la lucie roy",
                "morc lotus",
                "nsld bel air",
                "morc le florent",
                "route royale ernest florent",
                "chemin gandhi",
            ],
        ),
        (
            "Rose belle habitant dans le périmètre et les rues suivantes : Marie Jeannie, Madame Lolo, Janmohur Street, Kulpoo Lane, Railway Road, Capitol Lane, Mongelard Street, Morcellement Orchidée, EDC Rose Belle et une partie de la Route Royal Rose Belle",
            [
                "rose belle habitant dans le périmètre et les rues suivantes : marie jeannie",
                "madame lolo",
                "janmohur street",
                "kulpoo lane",
                "railway road",
                "capitol lane",
                "mongelard street",
                "morcellement orchidée",
                "edc rose belle",
                "une partie de la route royal rose belle",
            ],
        ),
        (
            "Une partie de Route Vingta No. 2 et No. 3, Kistoo Lane, Elaheebacus Lane.",
            [
                "une partie de route vingta no. 2 et no. 3",
                "kistoo lane",
                "elaheebacus lane",
            ],
        ),
        (
            "Le village de Riambel Surinam",
            ["le village de riambel surinam"],
        ),
        (
            "Le village de Riambel Surinam et les environs",
            ["le village de riambel surinam"],
        ),
        (
            "Le village de Riambel Surinam et les environs de st pierre",
            ["le village de riambel surinam", "st pierre"],
        ),
    ]

    @pytest.mark.parametrize("message,expected_result", testdata)
    def test_retrieve_ceb_streets(self, message, expected_result):
        # Act
        result = retrieve_ceb_streets(message)

        # Assert
        assert result == expected_result
