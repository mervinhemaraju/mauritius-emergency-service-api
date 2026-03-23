import requests
from bs4 import BeautifulSoup
from app.api.v1.utils.constant_urls import SUNRISE_SUNSET_URL
from app.api.v1.models.sunrise_sunset import SunriseSunset


class SunriseSunsetService:
    def __init__(self, request_timeout=15) -> None:
        response = requests.get(url=SUNRISE_SUNSET_URL, timeout=request_timeout)
        response.raise_for_status()
        self.soup = BeautifulSoup(response.content, "html.parser")

    def get_sunrise_sunset(self) -> list[SunriseSunset]:
        left_content = self.soup.select_one(".left_content")

        # * Find the correct table — it's the one whose first row contains "DATE"
        target_table = None
        for table in left_content.find_all("table"):
            first_row_text = table.find("tr").get_text(strip=True).upper()
            if "DATE" in first_row_text:
                target_table = table
                break

        if not target_table:
            return []

        rows = target_table.find_all("tr")

        # * Row 0: DATE | Month A (colspan=2) | Month B (colspan=2)
        # * Row 1: (empty) | SUNRISE | SUNSET | SUNRISE | SUNSET
        # * Row 2+: data rows

        # * Extract month names from the header — skip the DATE cell (index 0)
        header_cells = rows[0].find_all(["td", "th"])
        months = [
            cell.get_text(strip=True)
            for cell in header_cells
            if cell.get_text(strip=True) and cell.get_text(strip=True).upper() != "DATE"
        ]

        month_a = months[0] if len(months) > 0 else "Unknown"
        month_b = months[1] if len(months) > 1 else "Unknown"

        results = []

        for row in rows[2:]:  # skip both header rows
            cells = [td.get_text(strip=True) for td in row.find_all(["td", "th"])]

            # * Skip rows that don't have a numeric day in the first cell
            if not cells or not cells[0].isdigit():
                continue

            day = cells[0].zfill(2)

            # * Month A: cells[1]=sunrise, cells[2]=sunset
            if len(cells) > 2 and cells[1] and cells[2]:
                results.append(
                    SunriseSunset(
                        date=f"{day} {month_a}",
                        sunrise=cells[1],
                        sunset=cells[2],
                    )
                )

            # * Month B: cells[3]=sunrise, cells[4]=sunset (absent for e.g. day 31 in April)
            if len(cells) > 4 and cells[3] and cells[4]:
                results.append(
                    SunriseSunset(
                        date=f"{day} {month_b}",
                        sunrise=cells[3],
                        sunset=cells[4],
                    )
                )

        return results
