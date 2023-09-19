from flask_restful import Resource
from app.api.v1_0.models.cyclone import Cyclone
from app.messages.messages import CONTENT_NOT_FOUND_REPORT, content_cyclone_report

# * The Service class returns a
# * cyclone report


class CycloneReport(Resource):

    # > GET Request
    def get(self, lang):

        try:
            # * Create a new cyclone object
            cyclone = Cyclone(
                lang=lang
            )

            # * Create a cyclone report
            return (
                content_cyclone_report(
                    level=cyclone.class_level(),
                    next_bulletin=cyclone.next_bulletin(),
                    news=cyclone.news()
                ),
                200
            )
        except Exception as e:
            # * Update the content message
            error_content = CONTENT_NOT_FOUND_REPORT
            error_content['message'] = error_content['message'].format(str(e))
            return (
                error_content,
                404
            )
