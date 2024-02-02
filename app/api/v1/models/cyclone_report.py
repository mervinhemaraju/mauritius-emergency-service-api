from flask_restful import fields


class CycloneReport(object):
    cyclone_report_fields = {
        "level": fields.Integer,
        "next_bulletin": fields.String,
        "news": fields.List(fields.String),
    }

    def __init__(self, level, next_bulletin, news):
        self.level = level
        self.next_bulletin = next_bulletin
        self.news = news


class CycloneReportOutput(object):
    cyclone_report_output_fields = {
        "report": fields.Nested(CycloneReport.cyclone_report_fields, default=None),
        "message": fields.String,
        "success": fields.Boolean,
    }

    def __init__(self, report=None, message="", success=False) -> None:
        self.report = report
        self.message = message
        self.success = success
