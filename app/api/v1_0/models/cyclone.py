import requests
import re
from bs4 import BeautifulSoup
from app.api.v1_0.utils.helpers import (
    retrieve_cyclone_class_level,
    retrieve_time_from_text
)
from app.api.v1_0.models.exceptions import CycloneReportFailure
from app.api.v1_0.utils.constants import cyclone_report_url_def


class Cyclone:

    __level = {
        "N/A": 0,
        "I": 1,
        "II": 2,
        "III": 3,
        "IV": 4
    }

    def __init__(self, lang) -> None:

        # * Get the HTML page
        response = requests.get(
            url=cyclone_report_url_def[lang]
        )

        # * Verify if request was successful
        if (response.status_code != 200):
            raise CycloneReportFailure(
                "Error occurred while getting cyclone report"
            )

        # * Create a soup for the html page
        self.soup = BeautifulSoup(response.content, 'html.parser')

    def news(self):

        # * Retrieve the left content of the page
        left_content = self.soup.select_one(".left_content")

        # * Get all the p content of the page
        ps = left_content.find_all('p')

        # * Clean the paragraphs and return it
        return [
            p.text.strip().replace('\n', ' ').replace(' \xa0 ', '')
            for p in ps
            if p.text.strip() != ''
        ]

    def next_bulletin(self):

        # * Get the next bulletin time
        next_bulletin = self.soup.find(
            string=re.compile("The next bulletin will be issued")
        )

        # * Retrieve time from text and return
        return retrieve_time_from_text(next_bulletin)

    def class_level(self):

        # * Retrieve the left content of the page
        left_content = self.soup.select_one(".left_content")

        # * Get all the strong content of the page
        strongs = left_content.find_all('strong')

        # * Get the first element in the list
        message = next(filter(lambda x: x, strongs), None)

        # * Extract the class level in the message
        class_level = retrieve_cyclone_class_level(message, "class")

        # * Verify if it is not None
        if not class_level:
            return self.__level["N/A"]

        # * Return the class level
        return self.__level[class_level]
