import requests
import re
import json
from bs4 import BeautifulSoup
from app.api.v1.utils.helpers import (
    retrieve_cyclone_class_level,
    retrieve_time_from_text,
)
from app.api.v1.utils.constants import guidelines_json_file, guidelines_json_def
from app.api.v1.services.exceptions import CycloneReportFailure
from app.api.v1.utils.constants import cyclone_report_url_def
from app.api.v1.models.cyclone_name import CycloneName
from app.api.v1.models.cyclone_guidelines import CycloneGuideline


class Cyclone:
    __level = {"N/A": 0, "I": 1, "II": 2, "III": 3, "IV": 4}

    def __init__(self, lang, url=cyclone_report_url_def) -> None:
        # * Get the HTML page
        response = requests.get(url=url[lang])

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
        names_row = left_content.find("table").find("tbody").find_all("tr")

        # * Remove the table header
        del names_row[:1]

        # * Define empty list of names
        names: list[CycloneName] = []

        # * Format the names and return them in an array document
        for name in names_row:
            # * Get all the values in the td
            values = [value.get_text().strip() for value in name.find_all("td")]

            # * Delete column header
            del values[:1]

            # * Append the name document to the names list
            names.append(
                CycloneName(name=values[0], provided_by=values[1], named_by=values[2])
            )

        # * Return the names list
        return names


class CycloneGuidelines:
    def __init__(self, lang) -> None:
        self.lang = lang

    def load(self):
        # * Open the file according to the language queried
        with open(
            guidelines_json_file.get(self.lang, guidelines_json_def)
        ) as guidelines_file:
            # * Get the guidelines
            guidelines = json.load(guidelines_file)

            # * Format the guidelines into an object adn return it
            return [
                CycloneGuideline(
                    level=guideline["level"], description=guideline["description"]
                )
                for guideline in guidelines
            ]
