import re
import logging
from datetime import datetime
from dateutil import parser
from app.api.v1.utils.constant_others import MONTH_NUMBER_MAPPING_VARIANTS


def retrieve_ceb_streets(raw_streets):
    """
    Cleans and splits a raw string of street names into a list.

    This final version:
    1. Fixes double-escaped Unicode characters.
    2. Strips whitespace.
    3. **NEW:** Only removes "et les environs" if it's at the
       very end of the string.
    4. Splits by primary delimiters (comma, newline).
    5. **NEW:** Checks the last item for two types of separators,
       checking for the longer "et les environs de" first,
       then for "et".
    6. Strips trailing periods from all final items.
    """

    # 1. Fix Unicode and strip whitespace
    text = raw_streets.strip()

    # 2. NEW Rule:
    #    Only remove "et les environs" if it's at the very end.
    if text.lower().endswith("et les environs"):
        # Find the index of the last occurrence
        end_index = text.lower().rfind("et les environs")
        # Slice the string to remove it
        text = text[:end_index].strip()

    # 3. Now, lowercase the whole thing for processing
    text = text.lower()

    # 4. Split by primary delimiters (comma, newline)
    streets_list = [s.strip() for s in re.split(r"[,\n]", text) if s]

    # 5. Apply the refined 'et' separator logic.
    #    We must check for the longer "et les environs de" FIRST,
    #    otherwise "et" would match it incorrectly.
    separator_regex = r"\s+(?:et les environs de|et)\s+"

    if streets_list and re.search(separator_regex, streets_list[-1]):
        # Remove the last item to be split
        last_element = streets_list.pop()

        # Split *only that item* by the complex separator
        parts = re.split(separator_regex, last_element)

        # Add the new, split parts back to the list
        streets_list.extend(parts)

    # 6. Final clean-up: strip whitespace and trailing periods
    return [s.strip().rstrip(".") for s in streets_list if s.strip()]


def parse_ceb_datetimes(date_string):
    """
    Parses French datetime strings and extracts start and end datetimes.

    Args:
        date_string (str): String in format like "Le dimanche 26 octobre 2025 de 08:30:00 \\u00e0 14:00:00"

    Returns:
        tuple: (start_datetime, end_datetime) as datetime objects
    """
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
