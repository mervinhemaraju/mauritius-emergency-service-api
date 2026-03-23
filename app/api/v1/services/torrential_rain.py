import requests
from bs4 import BeautifulSoup
from app.api.v1.utils.constant_urls import TORRENTIAL_RAIN_ALERT_URL
from app.api.v1.models.torrential_rain import TorrentialRainAlert


class TorrentialRainAlertService:
    def __init__(self, request_timeout=15) -> None:
        response = requests.get(url=TORRENTIAL_RAIN_ALERT_URL, timeout=request_timeout)
        response.raise_for_status()

        self.soup = BeautifulSoup(response.content, "html.parser")

    def get_alert(self) -> TorrentialRainAlert | None:
        warning_div = self.soup.select_one(".warning")

        if not warning_div:
            return None

        # * Get all paragraphs from the warning div
        paragraphs = [
            p.get_text(strip=True)
            for p in warning_div.find_all("p")
            if p.get_text(strip=True)
        ]

        if not paragraphs:
            return None

        return TorrentialRainAlert(
            title=paragraphs[0],
        )
