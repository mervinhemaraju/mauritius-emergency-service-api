import requests
from bs4 import BeautifulSoup
from app.api.v1.utils.constant_urls import TIDES_URL
from app.api.v1.models.tides import Tide, TidesEntry

# * Known sub-header keywords to skip
_SKIP_KEYWORDS = ["date", "time", "height", "high tide", "low tide", "local"]


class TidesService:
    def __init__(self, request_timeout=15) -> None:
        response = requests.get(url=TIDES_URL, timeout=request_timeout)
        response.raise_for_status()
        self.soup = BeautifulSoup(response.content, "html.parser")

    def _parse_tide(self, time: str, height: str) -> Tide | None:
        if not time or not height or time == "-" or height == "-":
            return None
        return Tide(time=time, height_cm=height)

    def _is_month_header(self, cells: list[str]) -> str | None:
        # * A month header row has exactly one non-empty cell and it contains a year
        non_empty = [c for c in cells if c.strip()]
        if len(non_empty) == 1 and any(year in non_empty[0] for year in ["20", "19"]):
            return non_empty[0].strip()
        return None

    def _is_sub_header(self, cells: list[str]) -> bool:
        # * Sub-header rows contain known column label keywords
        joined = " ".join(cells).lower()
        return any(keyword in joined for keyword in _SKIP_KEYWORDS)

    def get_tides(self) -> list[TidesEntry]:
        left_content = self.soup.select_one(".left_content")

        # * Find the correct table — look for one containing "High Tide" or "Date"
        target_table = None
        for table in left_content.find_all("table"):
            table_text = table.get_text(strip=True).upper()
            if "HIGH TIDE" in table_text and "LOW TIDE" in table_text:
                target_table = table
                break

        if not target_table:
            return []

        rows = target_table.find_all("tr")
        results = []
        current_month = None

        for row in rows:
            cells = [td.get_text(strip=True) for td in row.find_all(["td", "th"])]

            if not cells:
                continue

            # * Check if this is a month header row
            month = self._is_month_header(cells)
            if month:
                current_month = month
                continue

            # * Skip sub-header rows
            if self._is_sub_header(cells):
                continue

            # * Skip rows where the first non-empty cell is not a digit
            first_cell = cells[0].strip()
            if not first_cell.isdigit():
                continue

            # * Need at least 9 cells for a full data row
            if len(cells) < 9:
                continue

            day = first_cell.zfill(2)
            date = f"{day} {current_month}" if current_month else day

            results.append(
                TidesEntry(
                    date=date,
                    high_tide_1=self._parse_tide(cells[1], cells[2]),
                    high_tide_2=self._parse_tide(cells[3], cells[4]),
                    low_tide_1=self._parse_tide(cells[5], cells[6]),
                    low_tide_2=self._parse_tide(cells[7], cells[8]),
                )
            )

        return results
