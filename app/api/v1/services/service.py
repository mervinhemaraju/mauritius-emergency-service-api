import json
from app.api.v1.utils.constants import json_file, json_def
from app.api.v1.models.services import Service as Service


class Services:
    def __init__(self, lang) -> None:
        self.lang = lang

    def load(self):
        # * Open the file according to the language queried
        with open(json_file.get(self.lang, json_def)) as services_file:
            # * Get the services
            services = json.load(services_file)

            # * Format the service into an object adn return it
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
