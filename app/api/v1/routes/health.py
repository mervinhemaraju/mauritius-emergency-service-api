from flask_restful import Resource


class HealthResource(Resource):
    # > GET Request
    def get(self):
        # Return simple health endpoint
        return {"status": "ok"}, 200
