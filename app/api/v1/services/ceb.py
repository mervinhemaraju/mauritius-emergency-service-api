import re
import codecs
import requests
from bs4 import BeautifulSoup
from app.api.v1.models.ceb_outage import (
    CebOutages as CebOutagesModel,
    CebOutage,
    CebOutageRaw,
)
from app.api.v1.services.exceptions import CebOutagesFailure
from app.api.v1.utils.helpers import parse_ceb_datetimes, retrieve_ceb_streets
from app.api.v1.utils.constant_urls import CEB_OUTAGES_URL
from app.api.v1.utils.constant_others import CEB_DISTRICTS


class Ceb:
    def __init__(self, url=CEB_OUTAGES_URL, request_timeout=15) -> None:
        # Fetch the page
        response = requests.get(url, timeout=request_timeout)
        response.raise_for_status()

        # * Verify if request was successful
        if response.status_code != 200:
            raise CebOutagesFailure("Error occurred while getting the CEB outages.")

        # Create a soup for the html page
        self.soup = BeautifulSoup(response.content, "html.parser")

    def get_outages(self):
        # Find the script tag containing arDistrictLocations
        script_tags = self.soup.find_all("script", type="text/javascript")

        # Define empty list of outages
        district_outages_list = []

        # Get each script in script tags
        for script in script_tags:
            # Check if the flag is present
            if script.string and "arDistrictLocations" in script.string:
                # Extract the JavaScript object
                script_content = script.string

                # Use regex to find the arDistrictLocations object
                match = re.search(
                    r"var arDistrictLocations = ({.*?});", script_content, re.DOTALL
                )

                if match:
                    js_object = match.group(1)

                    for district_key, district_name in CEB_DISTRICTS.items():
                        # Extract HTML for this district
                        pattern = f'"{district_key}":"(.*?)",'
                        district_match = re.search(pattern, js_object, re.DOTALL)

                        if district_match:
                            html_content = district_match.group(1)
                            # Unescape the HTML
                            html_content = (
                                html_content.replace(r"\/", "/")
                                .replace(r"\n", "\n")
                                .replace(r"\"", '"')
                            )

                            # Parse the HTML table
                            district_soup = BeautifulSoup(html_content, "html.parser")
                            table = district_soup.find("table")

                            outages = []
                            if table:
                                tbody = table.find("tbody")
                                if tbody:
                                    rows = tbody.find_all("tr")
                                    for row in rows:
                                        cells = row.find_all("td")
                                        if len(cells) == 3:
                                            date = codecs.decode(
                                                cells[0].get_text(strip=True),
                                                "unicode_escape",
                                            )
                                            locality = codecs.decode(
                                                cells[1].get_text(strip=True),
                                                "unicode_escape",
                                            )
                                            streets = codecs.decode(
                                                cells[2].get_text(strip=True),
                                                "unicode_escape",
                                            )

                                            # Only process if there's actual data
                                            if date and locality and streets:
                                                # Create raw outage object
                                                outage_raw = CebOutageRaw(
                                                    date=date,
                                                    locality=locality,
                                                    streets=streets,
                                                )

                                                # Process the streets list
                                                streets_list = retrieve_ceb_streets(
                                                    raw_streets=streets
                                                )

                                                # Parse datetime if date exists
                                                start_datetime = None
                                                end_datetime = None
                                                if date != "":
                                                    try:
                                                        (
                                                            start_datetime,
                                                            end_datetime,
                                                        ) = parse_ceb_datetimes(date)
                                                        print(
                                                            f"Date is {start_datetime} to {end_datetime}"
                                                        )
                                                    except Exception as e:
                                                        print(
                                                            f"Error parsing date: {e}"
                                                        )

                                                # Create outage object
                                                outage = CebOutage(
                                                    start_datetime=start_datetime,
                                                    end_datetime=end_datetime,
                                                    locality=locality,
                                                    streets=streets_list,
                                                    outages_raw=outage_raw,
                                                )
                                                outages.append(outage)

                            # Create district outages object
                            district_outages = CebOutagesModel(
                                district=district_name, outages=outages
                            )
                            district_outages_list.append(district_outages)

                    break

        # Return the list of outages
        return district_outages_list
