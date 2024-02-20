from flask_restful import fields


class Service(object):
    service_fields = {
        "identifier": fields.String,
        "name": fields.String,
        "type": fields.String,
        "icon": fields.String,
        "main_contact": fields.Integer,
        "emails": fields.List(fields.String),
        "other_contacts": fields.List(fields.Integer),
    }

    def __init__(
        self, identifier, name, type, icon, main_contact, emails, other_contacts
    ) -> None:
        self.identifier = identifier
        self.name = name
        self.type = type
        self.icon = icon
        self.main_contact = main_contact
        self.emails = emails
        self.other_contacts = other_contacts


class ServicesOutput(object):
    service_output_fields = {
        "services": fields.Nested(Service.service_fields, default=[]),
        "message": fields.String,
        "success": fields.Boolean,
    }

    def __init__(self, services=[], message="", success=False) -> None:
        self.services = services
        self.message = message
        self.success = success
