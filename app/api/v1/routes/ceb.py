import re
import requests
from flask_restful import Resource
from bs4 import BeautifulSoup
from app.api.v1.utils.helpers import parse_ceb_datetimes


class CebOutages(Resource):
    def get(self, lang):
        url = "https://ceb.mu/customer-corner/power-outage-information"

        # Fetch the page
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        # Parse HTML
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the script tag containing arDistrictLocations
        script_tags = soup.find_all("script", type="text/javascript")

        district_data = {}

        for script in script_tags:
            if script.string and "arDistrictLocations" in script.string:
                # Extract the JavaScript object
                script_content = script.string

                # Use regex to find the arDistrictLocations object
                match = re.search(
                    r"var arDistrictLocations = ({.*?});", script_content, re.DOTALL
                )

                if match:
                    js_object = match.group(1)

                    # Parse each district's HTML content
                    districts = {
                        "blackriver": "Black River",
                        "flacq": "Flacq",
                        "grandport": "Grand Port",
                        "moka": "Moka",
                        "pamplemousses": "Pamplemousses",
                        "plainewilhems": "Plaines Wilhems",
                        "portlouis": "Port Louis",
                        "rivieredurempart": "Rivière du Rempart",
                        "savanne": "Savanne",
                    }

                    for district_key, district_name in districts.items():
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
                                            date = cells[0].get_text(strip=True)
                                            locality = cells[1].get_text(strip=True)
                                            streets = cells[2].get_text(strip=True)

                                            if date != "":
                                                temp_sdate, temp_edate = (
                                                    parse_ceb_datetimes(date)
                                                )
                                                print(
                                                    f"Date is {temp_sdate} to {temp_edate}"
                                                )

                                            # Only add if there's actual data
                                            if date and locality and streets:
                                                outages.append(
                                                    {
                                                        "date": date,
                                                        "locality": locality,
                                                        "streets": streets,
                                                    }
                                                )

                            district_data[district_key] = {
                                "name": district_name,
                                "outages": outages,
                            }

                    break

        return district_data
