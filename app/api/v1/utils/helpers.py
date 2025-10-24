import re
import logging
from datetime import datetime
from dateutil import parser
from app.api.v1.utils.constant_others import MONTH_NUMBER_MAPPING_VARIANTS


def parse_ceb_datetimes(date_string):
    """
    Parses French datetime strings and extracts start and end datetimes.

    Args:
        date_string (str): String in format like "Le dimanche 26 octobre 2025 de 08:30:00 \\u00e0 14:00:00"

    Returns:
        tuple: (start_datetime, end_datetime) as datetime objects
    """

    # Decode data
    # date_string = date_string.encode().decode("unicode-escape").lower()
    if "\\u00e0" in date_string:
        date_string = date_string.replace("\\u00e0", "à")

    # Extract date components using regex
    # Pattern: Le <day> <day_num> <month> <year> de <start_time> à <end_time>
    pattern = (
        r"le \w+ (\d+) (\w+) (\d{4}) de\s+(\d{2}:\d{2}:\d{2})\s+à\s+(\d{2}:\d{2}:\d{2})"
    )

    # Search for matches
    match = re.search(pattern, date_string, re.IGNORECASE)

    # If no matches are found, return None
    if not match:
        # Log a warning
        logging.warning(
            f"Script couldn't get datetime data from the pattern in the string '{date_string}'"
        )

        # Return None
        return None, None

    # Retrieve the data
    day_num, month_name, year, start_time, end_time = match.groups()

    # Get the month number
    month = MONTH_NUMBER_MAPPING_VARIANTS.get(month_name.lower())

    # If month is not found, return None
    if not month:
        # Log a warning
        logging.warning(
            f"Script couldn't get a month number from the month name '{month_name}' and string data '{date_string}'"
        )

        # Return None
        return None, None

    # Create a start datetime object
    start_datetime = datetime.strptime(
        f"{year}-{month:02d}-{day_num} {start_time}", "%Y-%m-%d %H:%M:%S"
    )

    # Create an end datetime object
    end_datetime = datetime.strptime(
        f"{year}-{month:02d}-{day_num} {end_time}", "%Y-%m-%d %H:%M:%S"
    )

    # Return the date time objects
    return start_datetime, end_datetime


def retrieve_time_from_text(text):
    # * Parse the text to extract all times
    times = []

    for word in str(text).strip().split():
        try:
            time = parser.parse(word).strftime("%H:%M:%S")
            times.append(time)
        except ValueError:
            continue

    return times[0] if times is not None and len(times) > 0 else None


def retrieve_cyclone_class_level(message, keyword):
    # * Split the message into a list of words
    words = str(message).split()

    # * Iterate over the words and look for the phrase "class"
    # * followed by a Roman numeral
    for i in range(len(words)):
        if words[i] == keyword and i + 1 < len(words) and words[i + 1].isupper():
            return words[i + 1]

    # * Else return None
    return None


def sort_queried_service(args, services):
    # * Checks if an order was queried
    if "order" in args:
        order = args["order"]

        # * Checks order type
        if order == "asc":
            return sorted(services, key=lambda x: x["name"], reverse=False)
        if order == "dsc":
            return sorted(services, key=lambda x: x["name"], reverse=True)
    return services
