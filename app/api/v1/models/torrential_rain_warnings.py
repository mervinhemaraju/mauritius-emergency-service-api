from flask_restful import fields


class TorrentialRainWarningsSection(object):
    section_fields = {
        "id": fields.String,
        "title": fields.String,
        "content": fields.String,
        "stakeholders": fields.List(fields.String),
    }

    def __init__(self, id, title, content=None, stakeholders=None):
        self.id = id
        self.title = title
        self.content = content
        self.stakeholders = stakeholders


class TorrentialRainWarnings(object):
    torrential_rain_warnings_fields = {
        "id": fields.String,
        "title": fields.String,
        "sections": fields.List(
            fields.Nested(TorrentialRainWarningsSection.section_fields)
        ),
    }

    def __init__(self, id, title, sections):
        self.id = id
        self.title = title
        self.sections = sections


class TorrentialRainWarningsOutput(object):
    torrential_rain_warnings_output_fields = {
        "data": fields.Nested(
            TorrentialRainWarnings.torrential_rain_warnings_fields, default=None
        ),
        "message": fields.String,
        "success": fields.Boolean,
    }

    def __init__(self, data=None, message="", success=False):
        self.data = data
        self.message = message
        self.success = success
