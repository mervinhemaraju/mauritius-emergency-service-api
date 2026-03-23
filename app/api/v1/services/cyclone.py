import requests
import re
import json
from bs4 import BeautifulSoup
from app.api.v1.utils.helpers import (
    retrieve_cyclone_class_level,
    retrieve_time_from_text,
)
from app.api.v1.utils.constant_paths import guidelines_json_file
from app.api.v1.services.exceptions import CycloneReportFailure
from app.api.v1.utils.constant_urls import cyclone_report_url_def
from app.api.v1.models.cyclone_name import CycloneName
from app.api.v1.models.cyclone_guidelines import CycloneGuideline


class Cyclone:
    __level = {"N/A": 0, "I": 1, "II": 2, "III": 3, "IV": 4}

    def __init__(self, lang, url=cyclone_report_url_def, request_timeout=15) -> None:
        # * Get the HTML page
        response = requests.get(url=url[lang], timeout=request_timeout)
        response.raise_for_status()

        # * Verify if request was successful
        if response.status_code != 200:
            raise CycloneReportFailure("Error occurred while getting cyclone report")

        # * Create a soup for the html page
        self.soup = BeautifulSoup(response.content, "html.parser")

    def news(self) -> list[str]:
        # * Retrieve the left content of the page
        left_content = self.soup.select_one(".left_content")

        # * Get all the p content of the page
        ps = left_content.find_all("p")

        # * Clean the paragraphs and return it
        return [
            p.text.strip().replace("\n", " ").replace(" \xa0 ", "")
            for p in ps
            if p.text.strip() != ""
        ]

    def next_bulletin(self) -> str:
        # * Get the next bulletin time
        next_bulletin = self.soup.find(
            string=re.compile("The next bulletin will be issued")
        )

        # * Retrieve time from text and return
        return retrieve_time_from_text(next_bulletin)

    def class_level(self) -> int:
        # * Retrieve the left content of the page
        left_content = self.soup.select_one(".left_content")

        # * Get all the strong content of the page
        strongs = left_content.find_all("strong")

        # * Get the first element in the list
        message = next(filter(lambda x: x, strongs), None)

        # * Extract the class level in the message
        class_level = retrieve_cyclone_class_level(message, "class")

        # * Verify if it is not None
        if not class_level:
            return self.__level["N/A"]

        # * Return the class level
        return self.__level[class_level]

    def names(self) -> list[CycloneName]:
        # * Retrieve the left content of the page
        left_content = self.soup.select_one(".left_content")

        # * Retrieve the names row
        names_row: list = left_content.find("table").find("tbody").find_all("tr")

        print(f"{len(names_row)} names row are {names_row}")

        # Remove unused rows until names are obtained
        for i, row_html in enumerate(names_row):
            # We check a lowercase version to make it case-insensitive
            row_lower = row_html.get_text().lower()

            # Check if both keywords are in this row string
            if "names" in row_lower and "gender" in row_lower:
                # Found the header!
                # Return a new list starting from this index (i).
                names_row = names_row[i + 1 :]
                break

        # * Define empty list of names
        names: list[CycloneName] = []

        # * Format the names and return them in an array document
        for name in names_row:
            # * Get all the values in the td
            values = [value.get_text().strip() for value in name.find_all("td")]

            # * Delete column header
            del values[:1]

            # * Verify if values length is 4
            if len(values) < 4:
                continue

            # * Append the name document to the names list
            names.append(
                CycloneName(
                    name=values[1],
                    gender=values[2],
                    provided_by=values[3],
                )
            )

        # * Return the names list
        return names


class CycloneGuidelines:
    """
    The class that handles cyclone guidelines
    """

    def __init__(self, lang) -> None:
        self.lang = lang

    def load(self):
        # Define the default language
        default_lang_file = next(iter(guidelines_json_file.values()))

        # Open the file according to the language queried
        with open(
            guidelines_json_file.get(self.lang, default_lang_file)
        ) as guidelines_file:
            # Get the guidelines
            guidelines = json.load(guidelines_file)

            # Format the guidelines into an object adn return it
            return [
                CycloneGuideline(
                    level=guideline["level"],
                    description=guideline["description"],
                    precautions=guideline["precautions"],
                )
                for guideline in guidelines
            ]
