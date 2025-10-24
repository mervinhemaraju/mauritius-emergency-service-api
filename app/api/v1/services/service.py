import json
from app.api.v1.utils.constant_paths import json_file
from app.api.v1.models.services import Service as Service


class Services:
    """
    The class that loads the MES services from the json file based
    on the requested language
    """

    def __init__(self, lang) -> None:
        # The language requested
        self.lang = lang

    def load(self):
        # Define the default language
        default_lang_file = next(iter(json_file.values()))

        # Open the file according to the language queried
        with open(json_file.get(self.lang, default_lang_file)) as services_file:
            # Get the services
            services = json.load(services_file)

            # Format the service into an object adn return it
            return [
                Service(
                    identifier=service.get("identifier"),
                    name=service.get("name"),
                    type=service.get("type"),
                    icon=service.get("icon"),
                    main_contact=service.get("main_contact"),
                    emails=service.get("emails"),
                    other_contacts=service.get("other_contacts"),
                )
                for service in services
            ]
