import requests
from bs4 import BeautifulSoup
from app.api.v1.utils.constant_urls import MOONRISE_MOONSET_URL
from app.api.v1.models.moonrise_moonset import MoonriseMoonset


class MoonriseMoonsetService:
    def __init__(self, request_timeout=15) -> None:
        response = requests.get(url=MOONRISE_MOONSET_URL, timeout=request_timeout)
        response.raise_for_status()
        self.soup = BeautifulSoup(response.content, "html.parser")

    def get_moonrise_moonset(self) -> list[MoonriseMoonset]:
        left_content = self.soup.select_one(".left_content")

        # * Find the correct table — the one whose first row contains "DATE"
        target_table = None
        for table in left_content.find_all("table"):
            first_row_text = table.find("tr").get_text(strip=True).upper()
            if "DATE" in first_row_text:
                target_table = table
                break

        if not target_table:
            return []

        rows = target_table.find_all("tr")

        # * Row 0: DATE | Month A (colspan=3) | Month B (colspan=3)
        # * Row 1: (empty) | PHASE/TIME | MOON | (empty) | PHASE/TIME | MOON | (empty)
        # * Row 2: (empty) | RISE | TIME | RISE | SET
        # * Row 3+: data rows

        # * Extract month names — skip the DATE cell
        header_cells = rows[0].find_all(["td", "th"])
        months = [
            cell.get_text(strip=True)
            for cell in header_cells
            if cell.get_text(strip=True) and cell.get_text(strip=True).upper() != "DATE"
        ]

        month_a = months[0] if len(months) > 0 else "Unknown"
        month_b = months[1] if len(months) > 1 else "Unknown"

        results = []

        # * Data rows start at index 3 (skip 3 header rows)
        for row in rows[3:]:
            cells = [td.get_text(strip=True) for td in row.find_all(["td", "th"])]

            # * Skip rows that don't have a numeric day in the first cell
            if not cells or not cells[0].isdigit():
                continue

            day = cells[0].zfill(2)

            # * Month A: cells[1]=phase, cells[2]=moonrise, cells[3]=moonset
            if len(cells) > 3:
                results.append(
                    MoonriseMoonset(
                        date=f"{day} {month_a}",
                        phase=cells[1] or None,
                        moonrise=cells[2] if cells[2] != "-" else None,
                        moonset=cells[3] if cells[3] != "-" else None,
                    )
                )

            # * Month B: cells[4]=phase, cells[5]=moonrise, cells[6]=moonset
            if len(cells) > 6:
                results.append(
                    MoonriseMoonset(
                        date=f"{day} {month_b}",
                        phase=cells[4] or None,
                        moonrise=cells[5] if cells[5] != "-" else None,
                        moonset=cells[6] if cells[6] != "-" else None,
                    )
                )

        return results
