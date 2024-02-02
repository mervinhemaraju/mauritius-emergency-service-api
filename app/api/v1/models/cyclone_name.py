from flask_restful import fields


class CycloneName(object):
    cyclone_name_fields = {
        "name": fields.String,
        "provided_by": fields.String,
        "named_by": fields.String,
    }

    def __init__(self, name, provided_by, named_by):
        self.name = name if name != "" else "N/A"
        self.provided_by = provided_by if provided_by != "" else "N/A"
        self.named_by = named_by if named_by != "" else "N/A"


class CycloneNameOutput(object):
    cyclone_name_output_fields = {
        "names": fields.Nested(CycloneName.cyclone_name_fields, default=[]),
        "message": fields.String,
        "success": fields.Boolean,
    }

    def __init__(self, names=[], message="", success=False) -> None:
        self.names = names
        self.message = message
        self.success = success
