from flask_restful import Resource

# from flask_restful import fields, marshal_with
from app.api.v1.services.cyclone import Cyclone
from app.messages.messages import (
    CONTENT_NOT_FOUND_REPORT,
    CONTENT_NOT_FOUND_NAMES,
    content_cyclone_report,
    content_cyclone_names,
)
from app.api.v1.utils.constants import cyclone_names_url_def
# * The Service class returns a
# * cyclone report / cyclone names


class CycloneReport(Resource):
    # > GET Request
    def get(self, lang):
        try:
            # * Create a new cyclone object
            cyclone = Cyclone(lang=lang)

            # * Create a cyclone report
            return (
                content_cyclone_report(
                    level=cyclone.class_level(),
                    next_bulletin=cyclone.next_bulletin(),
                    news=cyclone.news(),
                ),
                200,
            )
        except Exception as e:
            # * Update the content message
            error_content = CONTENT_NOT_FOUND_REPORT
            error_content["message"] = error_content["message"].format(str(e))
            return (error_content, 404)


class CycloneNames(Resource):
    # > GET Request
    def get(self, lang):
        try:
            # * Create a new cyclone object
            cyclone = Cyclone(lang=lang, url=cyclone_names_url_def)

            # * Create a cyclone report
            return (content_cyclone_names(names=cyclone.names()), 200)
        except Exception as e:
            # * Update the content message
            error_content = CONTENT_NOT_FOUND_NAMES
            error_content["message"] = error_content["message"].format(str(e))
            return (error_content, 404)


# resource_fields = {"task": fields.String, "uri": fields.String}


# class TodoDao(object):
#     def __init__(self, todo_id, task):
#         self.todo_id = todo_id
#         self.task = task

#         # This field will not be sent in the response
#         self.status = "active"


# class CycloneTest(Resource):
#     @marshal_with(resource_fields)
#     def get(self, lang):
#         return TodoDao(todo_id="my_todo", task="Remember the milk")
