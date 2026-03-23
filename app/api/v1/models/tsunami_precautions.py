from flask_restful import fields


class TsunamiPrecautionsSection(object):
    section_fields = {
        "id": fields.String,
        "title": fields.String,
        "content": fields.String,
        "precautions": fields.List(fields.String),
    }

    def __init__(self, id, title, content=None, precautions=None):
        self.id = id
        self.title = title
        self.content = content
        self.precautions = precautions


class TsunamiPrecautions(object):
    tsunami_precautions_fields = {
        "id": fields.String,
        "title": fields.String,
        "sections": fields.List(
            fields.Nested(TsunamiPrecautionsSection.section_fields)
        ),
    }

    def __init__(self, id, title, sections):
        self.id = id
        self.title = title
        self.sections = sections


class TsunamiPrecautionsOutput(object):
    tsunami_precautions_output_fields = {
        "data": fields.Nested(
            TsunamiPrecautions.tsunami_precautions_fields, default=None
        ),
        "message": fields.String,
        "success": fields.Boolean,
    }

    def __init__(self, data=None, message="", success=False):
        self.data = data
        self.message = message
        self.success = success
