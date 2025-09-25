import pytest
from bs4 import BeautifulSoup
from app.api.v1.services.cyclone import Cyclone
from app.api.v1.services.exceptions import CycloneReportFailure
from app.api.v1.utils.constants import cyclone_names_url_def


class TestServiceCyclone:
    testdata = [
        (
            "tests/v1/dummy_data/names/cyclone_names_1.html",
            [
                '{"name": "AWO", "gender": "N", "provided_by": "Malawi"}',
                '{"name": "BLOSSOM", "gender": "F", "provided_by": "Seychelles"}',
            ],
        ),
        (
            "tests/v1/dummy_data/names/cyclone_names_2.html",
            [
                '{"name": "INDUSA", "gender": "F", "provided_by": "Kenya"}',
                '{"name": "JULUKA", "gender": "M", "provided_by": "Eswatini"}',
                '{"name": "KUNDAI", "gender": "M", "provided_by": "Zimbabwe"}',
                '{"name": "LISEBO", "gender": "F", "provided_by": "Lesotho"}',
                '{"name": "MICHEL", "gender": "M", "provided_by": "France"}',
            ],
        ),
    ]

    @pytest.mark.parametrize("file,expected_result", testdata)
    def test_get_names(self, file, expected_result):
        # Act
        page = open(file, "r").read()

        cyclone = Cyclone(lang="en", url=cyclone_names_url_def)
        cyclone.soup = BeautifulSoup(page, "html.parser")
        result = cyclone.names()
        cyclones = [str(cyc) for cyc in result]

        # Assert
        assert expected_result == cyclones

    testdata = [
        ("tests/v1/dummy_data/levels/cyclone_class_1.html", "23:00:00"),
        ("tests/v1/dummy_data/levels/cyclone_class_2.html", "22:10:00"),
        ("tests/v1/dummy_data/levels/cyclone_class_3.html", "12:10:00"),
        ("tests/v1/dummy_data/levels/cyclone_class_4.html", "22:10:00"),
        ("tests/v1/dummy_data/levels/cyclone_class_none.html", None),
    ]

    @pytest.mark.parametrize("file,expected_result", testdata)
    def test_get_next_bulletin(self, file, expected_result):
        # Act
        page = open(file, "r").read()

        cyclone = Cyclone(lang="en")
        cyclone.soup = BeautifulSoup(page, "html.parser")
        result = cyclone.next_bulletin()

        # Assert
        assert result == expected_result

    testdata = [
        ("tests/v1/dummy_data/levels/cyclone_class_1.html", 1),
        ("tests/v1/dummy_data/levels/cyclone_class_2.html", 2),
        ("tests/v1/dummy_data/levels/cyclone_class_3.html", 3),
        ("tests/v1/dummy_data/levels/cyclone_class_4.html", 4),
        ("tests/v1/dummy_data/levels/cyclone_class_none.html", 0),
    ]

    @pytest.mark.parametrize("file,expected_result", testdata)
    def test_get_class_level(self, file, expected_result):
        # Act
        try:
            page = open(file, "r").read()

            cyclone = Cyclone(lang="en")
            cyclone.soup = BeautifulSoup(page, "html.parser")
            result = cyclone.class_level()
        except CycloneReportFailure as e:
            result = str(e)

        # Assert
        assert result == expected_result

        testdata = [
            ("tests/v1.0/dummy_data/cyclone_class_1.html", []),
            # ("tests/v1.0/dummy_data/cyclone_class_2.html", 2),
            # ("tests/v1.0/dummy_data/cyclone_class_3.html", 3),
            # ("tests/v1.0/dummy_data/cyclone_class_4.html", 4),
            # ("tests/v1.0/dummy_data/cyclone_class_none.html", 0),
        ]

    testdata = [
        (
            "tests/v1/dummy_data/levels/cyclone_class_1.html",
            [
                "Un avertissement de cyclone de Classe 2 est en vigueur a Maurice.                              | Un avertissement de cyclone de Classe 3 est en vigueur a                                 Rodrigues.",
                "Sun, Feb 19, 2023 A cyclone warning class I is in force in Mauritius                         A cyclone warning class I is in force in Mauritius  Fifth cyclone bulletin for Mauritius issued at 1610 hours on Sunday 19 February                         2023                      Over the last 6 hours Freddy has continued to weaken and is now an intense tropical cyclone. It has                     also accelerated with a slight recurvature in its trajectory towards the south.                      The estimated central pressure of Freddy is around 930 hPa and the estimated wind gusts near its                     centre is about 280 km/h.                      At 1600 hours, intense tropical cyclone Freddy was centred at about 720 km to the east-north-east of                     Mauritius near latitude 17.3 degrees south and longitude 64.1 degrees east.                      It is moving in a west south westerly direction at a speed of about 25 km/h.                       On this new trajectory Freddy is dangerously approaching Mauritius and may represent direct threat                     to the island. It may pass at about 140 km at its closest distance to the north north west of the                     island on Monday evening.  A cyclone warning class I is in force in Mauritius.                      The public in Mauritius is advised to complete all preliminary precautions.                      Weather will be partly cloudy to cloudy with passing showers mainly to the east and over the central                     plateau.                      Wind will blow from the southeast at a speed of about 30 km/h.                      Sea will become gradually rough beyond the reefs tonight with swells. It is advised not to venture                     in the open sea as from tonight.                      The weather conditions are expected to deteriorate rapidly in the early afternoon tomorrow, Monday                     20, with intermittent rain and gusts of the order of 100km/h.                      The sea will become very rough to high with heavy swells tomorrow morning.   A cyclone warning class I is in force in Mauritius                         A cyclone warning class I is in force in Mauritius.                      If intense tropical cyclone Freddy maintains this trajectory towards the west south west, the                     warning bulletin may be upgraded to class II at 0410 hours tomorrow morning.                      The next bulletin will be issued at around 23h00.",
                "A cyclone warning class I is in force in Mauritius                         A cyclone warning class I is in force in Mauritius  Fifth cyclone bulletin for Mauritius issued at 1610 hours on Sunday 19 February                         2023                      Over the last 6 hours Freddy has continued to weaken and is now an intense tropical cyclone. It has                     also accelerated with a slight recurvature in its trajectory towards the south.                      The estimated central pressure of Freddy is around 930 hPa and the estimated wind gusts near its                     centre is about 280 km/h.                      At 1600 hours, intense tropical cyclone Freddy was centred at about 720 km to the east-north-east of                     Mauritius near latitude 17.3 degrees south and longitude 64.1 degrees east.                      It is moving in a west south westerly direction at a speed of about 25 km/h.                       On this new trajectory Freddy is dangerously approaching Mauritius and may represent direct threat                     to the island. It may pass at about 140 km at its closest distance to the north north west of the                     island on Monday evening.  A cyclone warning class I is in force in Mauritius.                      The public in Mauritius is advised to complete all preliminary precautions.                      Weather will be partly cloudy to cloudy with passing showers mainly to the east and over the central                     plateau.                      Wind will blow from the southeast at a speed of about 30 km/h.                      Sea will become gradually rough beyond the reefs tonight with swells. It is advised not to venture                     in the open sea as from tonight.                      The weather conditions are expected to deteriorate rapidly in the early afternoon tomorrow, Monday                     20, with intermittent rain and gusts of the order of 100km/h.                      The sea will become very rough to high with heavy swells tomorrow morning.   A cyclone warning class I is in force in Mauritius                         A cyclone warning class I is in force in Mauritius.                      If intense tropical cyclone Freddy maintains this trajectory towards the west south west, the                     warning bulletin may be upgraded to class II at 0410 hours tomorrow morning.                      The next bulletin will be issued at around 23h00.",
            ],
        ),
        (
            "tests/v1/dummy_data/levels/cyclone_class_2.html",
            [
                "Un avertissement de cyclone de Classe 2 est en vigueur a Maurice.                              | Un avertissement de cyclone de Classe 3 est en vigueur a                                 Rodrigues.",
                "Sun, Feb 19, 2023 A cyclone warning class II is in force in Mauritius                         A cyclone warning class II is in force in Mauritius  Fifth cyclone bulletin for Mauritius issued at 1610 hours on Sunday 19 February                         2023                      Over the last 6 hours Freddy has continued to weaken and is now an intense tropical cyclone. It has                     also accelerated with a slight recurvature in its trajectory towards the south.                      The estimated central pressure of Freddy is around 930 hPa and the estimated wind gusts near its                     centre is about 280 km/h.                      At 1600 hours, intense tropical cyclone Freddy was centred at about 720 km to the east-north-east of                     Mauritius near latitude 17.3 degrees south and longitude 64.1 degrees east.                      It is moving in a west south westerly direction at a speed of about 25 km/h.                       On this new trajectory Freddy is dangerously approaching Mauritius and may represent direct threat                     to the island. It may pass at about 140 km at its closest distance to the north north west of the                     island on Monday evening.  A cyclone warning class II is in force in Mauritius.                      The public in Mauritius is advised to complete all preliminary precautions.                      Weather will be partly cloudy to cloudy with passing showers mainly to the east and over the central                     plateau.                      Wind will blow from the southeast at a speed of about 30 km/h.                      Sea will become gradually rough beyond the reefs tonight with swells. It is advised not to venture                     in the open sea as from tonight.                      The weather conditions are expected to deteriorate rapidly in the early afternoon tomorrow, Monday                     20, with intermittent rain and gusts of the order of 100km/h.                      The sea will become very rough to high with heavy swells tomorrow morning.   A cyclone warning class II is in force in Mauritius                         A cyclone warning class II is in force in Mauritius.                      If intense tropical cyclone Freddy maintains this trajectory towards the west south west, the                     warning bulletin may be upgraded to Class III at 0410 hours tomorrow morning.                      The next bulletin will be issued at around 22h10.",
                "A cyclone warning class II is in force in Mauritius                         A cyclone warning class II is in force in Mauritius  Fifth cyclone bulletin for Mauritius issued at 1610 hours on Sunday 19 February                         2023                      Over the last 6 hours Freddy has continued to weaken and is now an intense tropical cyclone. It has                     also accelerated with a slight recurvature in its trajectory towards the south.                      The estimated central pressure of Freddy is around 930 hPa and the estimated wind gusts near its                     centre is about 280 km/h.                      At 1600 hours, intense tropical cyclone Freddy was centred at about 720 km to the east-north-east of                     Mauritius near latitude 17.3 degrees south and longitude 64.1 degrees east.                      It is moving in a west south westerly direction at a speed of about 25 km/h.                       On this new trajectory Freddy is dangerously approaching Mauritius and may represent direct threat                     to the island. It may pass at about 140 km at its closest distance to the north north west of the                     island on Monday evening.  A cyclone warning class II is in force in Mauritius.                      The public in Mauritius is advised to complete all preliminary precautions.                      Weather will be partly cloudy to cloudy with passing showers mainly to the east and over the central                     plateau.                      Wind will blow from the southeast at a speed of about 30 km/h.                      Sea will become gradually rough beyond the reefs tonight with swells. It is advised not to venture                     in the open sea as from tonight.                      The weather conditions are expected to deteriorate rapidly in the early afternoon tomorrow, Monday                     20, with intermittent rain and gusts of the order of 100km/h.                      The sea will become very rough to high with heavy swells tomorrow morning.   A cyclone warning class II is in force in Mauritius                         A cyclone warning class II is in force in Mauritius.                      If intense tropical cyclone Freddy maintains this trajectory towards the west south west, the                     warning bulletin may be upgraded to Class III at 0410 hours tomorrow morning.                      The next bulletin will be issued at around 22h10.",
            ],
        ),
        (
            "tests/v1/dummy_data/levels/cyclone_class_3.html",
            [
                "Un avertissement de cyclone de Classe 2 est en vigueur a Maurice.                              | Un avertissement de cyclone de Classe 3 est en vigueur a                                 Rodrigues.",
                "Sun, Feb 19, 2023 A cyclone warning class III is in force in Mauritius                         A cyclone warning class III is in force in Mauritius  Fifth cyclone bulletin for Mauritius issued at 1610 hours on Sunday 19 February                         2023                      Over the last 6 hours Freddy has continued to weaken and is now an intense tropical cyclone. It has                     also accelerated with a slight recurvature in its trajectory towards the south.                      The estimated central pressure of Freddy is around 930 hPa and the estimated wind gusts near its                     centre is about 280 km/h.                      At 1600 hours, intense tropical cyclone Freddy was centred at about 720 km to the east-north-east of                     Mauritius near latitude 17.3 degrees south and longitude 64.1 degrees east.                      It is moving in a west south westerly direction at a speed of about 25 km/h.                       On this new trajectory Freddy is dangerously approaching Mauritius and may represent direct threat                     to the island. It may pass at about 140 km at its closest distance to the north north west of the                     island on Monday evening.  A cyclone warning class III is in force in Mauritius.                      The public in Mauritius is advised to complete all preliminary precautions.                      Weather will be partly cloudy to cloudy with passing showers mainly to the east and over the central                     plateau.                      Wind will blow from the southeast at a speed of about 30 km/h.                      Sea will become gradually rough beyond the reefs tonight with swells. It is advised not to venture                     in the open sea as from tonight.                      The weather conditions are expected to deteriorate rapidly in the early afternoon tomorrow, Monday                     20, with intermittent rain and gusts of the order of 100km/h.                      The sea will become very rough to high with heavy swells tomorrow morning.   A cyclone warning class III is in force in Mauritius                         A cyclone warning class III is in force in Mauritius.                      If intense tropical cyclone Freddy maintains this trajectory towards the west south west, the                     warning bulletin may be upgraded to class IIII at 0410 hours tomorrow morning.                      The next bulletin will be issued at around 12h10.",
                "A cyclone warning class III is in force in Mauritius                         A cyclone warning class III is in force in Mauritius  Fifth cyclone bulletin for Mauritius issued at 1610 hours on Sunday 19 February                         2023                      Over the last 6 hours Freddy has continued to weaken and is now an intense tropical cyclone. It has                     also accelerated with a slight recurvature in its trajectory towards the south.                      The estimated central pressure of Freddy is around 930 hPa and the estimated wind gusts near its                     centre is about 280 km/h.                      At 1600 hours, intense tropical cyclone Freddy was centred at about 720 km to the east-north-east of                     Mauritius near latitude 17.3 degrees south and longitude 64.1 degrees east.                      It is moving in a west south westerly direction at a speed of about 25 km/h.                       On this new trajectory Freddy is dangerously approaching Mauritius and may represent direct threat                     to the island. It may pass at about 140 km at its closest distance to the north north west of the                     island on Monday evening.  A cyclone warning class III is in force in Mauritius.                      The public in Mauritius is advised to complete all preliminary precautions.                      Weather will be partly cloudy to cloudy with passing showers mainly to the east and over the central                     plateau.                      Wind will blow from the southeast at a speed of about 30 km/h.                      Sea will become gradually rough beyond the reefs tonight with swells. It is advised not to venture                     in the open sea as from tonight.                      The weather conditions are expected to deteriorate rapidly in the early afternoon tomorrow, Monday                     20, with intermittent rain and gusts of the order of 100km/h.                      The sea will become very rough to high with heavy swells tomorrow morning.   A cyclone warning class III is in force in Mauritius                         A cyclone warning class III is in force in Mauritius.                      If intense tropical cyclone Freddy maintains this trajectory towards the west south west, the                     warning bulletin may be upgraded to class IIII at 0410 hours tomorrow morning.                      The next bulletin will be issued at around 12h10.",
            ],
        ),
        (
            "tests/v1/dummy_data/levels/cyclone_class_4.html",
            [
                "Un avertissement de cyclone de Classe 2 est en vigueur a Maurice.                              | Un avertissement de cyclone de Classe 3 est en vigueur a                                 Rodrigues.",
                "Sun, Feb 19, 2023 A cyclone warning class IV is in force in Mauritius                         A cyclone warning class IV is in force in Mauritius  Fifth cyclone bulletin for Mauritius issued at 1610 hours on Sunday 19 February                         2023                      Over the last 6 hours Freddy has continued to weaken and is now an intense tropical cyclone. It has                     also accelerated with a slight recurvature in its trajectory towards the south.                      The estimated central pressure of Freddy is around 930 hPa and the estimated wind gusts near its                     centre is about 280 km/h.                      At 1600 hours, intense tropical cyclone Freddy was centred at about 720 km to the east-north-east of                     Mauritius near latitude 17.3 degrees south and longitude 64.1 degrees east.                      It is moving in a west south westerly direction at a speed of about 25 km/h.                       On this new trajectory Freddy is dangerously approaching Mauritius and may represent direct threat                     to the island. It may pass at about 140 km at its closest distance to the north north west of the                     island on Monday evening.  A cyclone warning class IV is in force in Mauritius.                      The public in Mauritius is advised to complete all preliminary precautions.                      Weather will be partly cloudy to cloudy with passing showers mainly to the east and over the central                     plateau.                      Wind will blow from the southeast at a speed of about 30 km/h.                      Sea will become gradually rough beyond the reefs tonight with swells. It is advised not to venture                     in the open sea as from tonight.                      The weather conditions are expected to deteriorate rapidly in the early afternoon tomorrow, Monday                     20, with intermittent rain and gusts of the order of 100km/h.                      The sea will become very rough to high with heavy swells tomorrow morning.   A cyclone warning class IV is in force in Mauritius                         A cyclone warning class IV is in force in Mauritius.                      If intense tropical cyclone Freddy maintains this trajectory towards the west south west, the                     warning bulletin may be upgraded to class IVI at 0410 hours tomorrow morning.                      The next bulletin will be issued at around 22h10.",
                "A cyclone warning class IV is in force in Mauritius                         A cyclone warning class IV is in force in Mauritius  Fifth cyclone bulletin for Mauritius issued at 1610 hours on Sunday 19 February                         2023                      Over the last 6 hours Freddy has continued to weaken and is now an intense tropical cyclone. It has                     also accelerated with a slight recurvature in its trajectory towards the south.                      The estimated central pressure of Freddy is around 930 hPa and the estimated wind gusts near its                     centre is about 280 km/h.                      At 1600 hours, intense tropical cyclone Freddy was centred at about 720 km to the east-north-east of                     Mauritius near latitude 17.3 degrees south and longitude 64.1 degrees east.                      It is moving in a west south westerly direction at a speed of about 25 km/h.                       On this new trajectory Freddy is dangerously approaching Mauritius and may represent direct threat                     to the island. It may pass at about 140 km at its closest distance to the north north west of the                     island on Monday evening.  A cyclone warning class IV is in force in Mauritius.                      The public in Mauritius is advised to complete all preliminary precautions.                      Weather will be partly cloudy to cloudy with passing showers mainly to the east and over the central                     plateau.                      Wind will blow from the southeast at a speed of about 30 km/h.                      Sea will become gradually rough beyond the reefs tonight with swells. It is advised not to venture                     in the open sea as from tonight.                      The weather conditions are expected to deteriorate rapidly in the early afternoon tomorrow, Monday                     20, with intermittent rain and gusts of the order of 100km/h.                      The sea will become very rough to high with heavy swells tomorrow morning.   A cyclone warning class IV is in force in Mauritius                         A cyclone warning class IV is in force in Mauritius.                      If intense tropical cyclone Freddy maintains this trajectory towards the west south west, the                     warning bulletin may be upgraded to class IVI at 0410 hours tomorrow morning.                      The next bulletin will be issued at around 22h10.",
            ],
        ),
        (
            "tests/v1/dummy_data/levels/cyclone_class_none.html",
            [
                "A High wave warning is in force in Mauritius.  |  Heavy Rain Watch for Rodrigues issued at 10h00 on Saturday 27                                 January 2024",
                "Thu, Jan 25, 2024 No cyclone warning is in force in Mauritius                         No cyclone warning is in force in Mauritius  Fourteenth and last cyclone bulletin for Mauritius issued at 13h10 hours on Thursday 25                         January 2024.                      All weather observations at Mauritius show that moderate tropical storm Candice is moving further                     away from our region.                      At 1300 hours, it was centred at about 350 km to the southeast of Mauritius, that is, near latitude                     22.6 degres south and longitude 59.9 degrees east. Candice is moving in a general southeasterly                     track at a speed of about 24 km/h.\xa0\xa0\xa0\xa0\xa0 No cyclone warning is in force in Mauritius                      Cloud in the outermost circulation of Candice will continue to influence weather over the island                     giving intermittent rain, mainly over the high grounds. The rains may become locally moderate.                      Sea will remain very rough with swells of 4 metres beyond the reefs. Storm surges may impact the                     eastern, southern and western coastal areas. The public is strongly advised to be cautious and not                     to venture out at sea as well as along the beaches.                      For additional information, the public is advised to consult the regular bulletins issued by the                     Mauritius Meteorlogical Services.  No cyclone warning is in force in Mauritius",
                "No cyclone warning is in force in Mauritius                         No cyclone warning is in force in Mauritius  Fourteenth and last cyclone bulletin for Mauritius issued at 13h10 hours on Thursday 25                         January 2024.                      All weather observations at Mauritius show that moderate tropical storm Candice is moving further                     away from our region.                      At 1300 hours, it was centred at about 350 km to the southeast of Mauritius, that is, near latitude                     22.6 degres south and longitude 59.9 degrees east. Candice is moving in a general southeasterly                     track at a speed of about 24 km/h.\xa0\xa0\xa0\xa0\xa0 No cyclone warning is in force in Mauritius                      Cloud in the outermost circulation of Candice will continue to influence weather over the island                     giving intermittent rain, mainly over the high grounds. The rains may become locally moderate.                      Sea will remain very rough with swells of 4 metres beyond the reefs. Storm surges may impact the                     eastern, southern and western coastal areas. The public is strongly advised to be cautious and not                     to venture out at sea as well as along the beaches.                      For additional information, the public is advised to consult the regular bulletins issued by the                     Mauritius Meteorlogical Services.  No cyclone warning is in force in Mauritius",
            ],
        ),
    ]

    @pytest.mark.parametrize("file,expected_result", testdata)
    def test_get_news(self, file, expected_result):
        # Act
        try:
            page = open(file, "r").read()

            cyclone = Cyclone(lang="en")
            cyclone.soup = BeautifulSoup(page, "html.parser")
            result = cyclone.news()
            print(result)
        except CycloneReportFailure as e:
            result = str(e)

        # Assert
        assert result == expected_result
