from flask_restful import fields


class TsunamiWarningsStage(object):
    stage_fields = {
        "id": fields.String,
        "level": fields.Integer,
        "title": fields.String,
        "content": fields.String,
        "instructions": fields.List(fields.String),
    }

    def __init__(self, id, level, title, content=None, instructions=None):
        self.id = id
        self.level = level
        self.title = title
        self.content = content
        self.instructions = instructions


class TsunamiWarningsSection(object):
    section_fields = {
        "id": fields.String,
        "title": fields.String,
        "content": fields.String,
        "stages": fields.List(fields.Nested(TsunamiWarningsStage.stage_fields)),
    }

    def __init__(self, id, title, content=None, stages=None):
        self.id = id
        self.title = title
        self.content = content
        self.stages = stages


class TsunamiWarnings(object):
    tsunami_warnings_fields = {
        "id": fields.String,
        "title": fields.String,
        "sections": fields.List(fields.Nested(TsunamiWarningsSection.section_fields)),
    }

    def __init__(self, id, title, sections):
        self.id = id
        self.title = title
        self.sections = sections


class TsunamiWarningsOutput(object):
    tsunami_warnings_output_fields = {
        "data": fields.Nested(TsunamiWarnings.tsunami_warnings_fields, default=None),
        "message": fields.String,
        "success": fields.Boolean,
    }

    def __init__(self, data=None, message="", success=False):
        self.data = data
        self.message = message
        self.success = success
