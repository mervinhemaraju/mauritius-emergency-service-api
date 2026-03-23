import requests
from bs4 import BeautifulSoup
from app.api.v1.utils.constant_urls import TORRENTIAL_RAIN_ALERT_URL

_NON_ALERT_HREFS = ["index.php", "index.html", "/"]


class GeneralAlertService:
    def __init__(self, request_timeout=15) -> None:
        response = requests.get(url=TORRENTIAL_RAIN_ALERT_URL, timeout=request_timeout)
        response.raise_for_status()
        self.soup = BeautifulSoup(response.content, "html.parser")

    def get_alert(self) -> str | None:
        warning_div = self.soup.select_one(".warning")
        if not warning_div:
            return None

        marquee = warning_div.select_one("marquee")
        if not marquee:
            return None

        for anchor in marquee.find_all("a", href=True):
            href = anchor["href"].strip()

            if any(href.rstrip("/").endswith(page) for page in _NON_ALERT_HREFS):
                continue

            red_span = anchor.find("span", style=lambda s: s and "ff0000" in s.lower())
            if not red_span:
                continue

            alert_text = red_span.get_text(strip=True)
            if alert_text:
                return alert_text

        return None
