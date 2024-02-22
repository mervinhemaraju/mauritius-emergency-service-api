from flask_restful import fields


class CycloneGuideline(object):
    cyclone_guideline_fields = {"level": fields.String, "description": fields.String}

    def __init__(self, level, description):
        self.level = level
        self.description = description


class CycloneGuidelinesOutput(object):
    cyclone_guideline_output_fields = {
        "guidelines": fields.Nested(
            CycloneGuideline.cyclone_guideline_fields, default=[]
        ),
        "message": fields.String,
        "success": fields.Boolean,
    }

    def __init__(self, guidelines=[], message="", success=False) -> None:
        self.guidelines = guidelines
        self.message = message
        self.success = success
