import json
from flask_restful import fields


class CycloneName(object):
    cyclone_name_fields = {
        "name": fields.String,
        "gender": fields.String,
        "provided_by": fields.String,
    }

    def __init__(self, name, gender, provided_by):
        self.name = name if name != "" else "N/A"
        self.gender = gender if gender != "" else "N/A"
        self.provided_by = provided_by if provided_by != "" else "N/A"

    def __str__(self) -> str:
        return json.dumps(
            {
                "name": self.name,
                "gender": self.gender,
                "provided_by": self.provided_by,
            }
        )


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
