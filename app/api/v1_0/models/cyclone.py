import requests, re
from bs4 import BeautifulSoup
from app.api.v1_0.utils.helpers import retrieve_cyclone_class_level
from app.api.v1_0.models.exceptions import CycloneReportFailure

class Cyclone:

    level = {
        "I": 1,
        "II": 2,
        "III": 3,
        "IV": 4
    }

    def __init__(self) -> None:
        
        # * Create Url for the cyclone report website
        url = "http://metservice.intnet.mu/cyclone-bulletin-english-mauritius.php"

        # * Get the HTML page
        response = requests.get(url=url)

        # * Verify if request was successful
        if(response.status_code != 200):
            raise Exception("Error url")

        # * Create a soup for the html page
        self.soup = BeautifulSoup(response.content, 'html.parser')
    
    def next_bulletin(self):

        # * Get the next bulletin time
        next_bulletin = self.soup.find(string=re.compile("The next bulletin will be issued"))
        
        # * Verify if not None and return
        return next_bulletin.strip() if next_bulletin else next_bulletin
    
    def class_level(self):

        # * Retrieve the left content of the page
        left_content = self.soup.select_one(".left_content")

        # * Get all the strong content of the page
        strongs = left_content.find_all('strong')
        
        # * Get the first element in the list
        message = next(filter(lambda x: x, strongs), None)
        
        # * Extract the class level in the message
        class_level = retrieve_cyclone_class_level(message)

        # * Verify if it is not None
        if not class_level:
            raise CycloneReportFailure("Could not retrieve cyclone level.")

        # * Return the class level
        return self.level[class_level]
        

