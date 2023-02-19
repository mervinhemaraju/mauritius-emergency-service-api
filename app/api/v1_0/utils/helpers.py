
def retrieve_cyclone_class_level(message):

    # * Split the message into a list of words
    words = str(message).split()

    # * Iterate over the words and look for the phrase "class" followed by a Roman numeral
    for i in range(len(words)):
        if words[i] == "class" and i+1 < len(words) and words[i+1].isupper():
            return words[i+1]

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