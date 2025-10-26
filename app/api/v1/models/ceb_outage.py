from flask_restful import fields


class CebOutageRaw(object):
    ceb_outage_raw_fields = {
        "date": fields.String,
        "locality": fields.String,
        "streets": fields.String,
    }

    def __init__(self, date, locality, streets):
        self.date = date
        self.locality = locality
        self.streets = streets


class CebOutage(object):
    ceb_outage_fields = {
        "start_datetime": fields.String,
        "end_datetime": fields.String,
        "locality": fields.String,
        "streets": fields.List(fields.String),
        "_raw": fields.Nested(CebOutageRaw.ceb_outage_raw_fields, default=None),
    }

    def __init__(self, start_datetime, end_datetime, locality, streets, outages_raw):
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
        self.locality = locality
        self.streets = streets
        self._raw = outages_raw


class CebOutages(object):
    ceb_outages_fields = {
        "district": fields.String,
        "outages": fields.List(
            fields.Nested(CebOutage.ceb_outage_fields, default=None)
        ),
    }

    def __init__(self, district, outages):
        self.district = district
        self.outages = outages


class CebOutagesOutput(object):
    ceb_outages_output_fields = {
        "district_outages": fields.List(
            fields.Nested(CebOutages.ceb_outages_fields, default=None)
        ),
        "message": fields.String,
        "success": fields.Boolean,
    }

    def __init__(self, district_outages=None, message="", success=False) -> None:
        self.district_outages = district_outages
        self.message = message
        self.success = success


class CebOutagesByDistrictOutput(object):
    ceb_outages_by_district_output_fields = {
        "outages": fields.List(
            fields.Nested(CebOutage.ceb_outage_fields, default=None)
        ),
        "message": fields.String,
        "success": fields.Boolean,
    }

    def __init__(self, outages=None, message="", success=False) -> None:
        self.outages = outages
        self.message = message
        self.success = success
