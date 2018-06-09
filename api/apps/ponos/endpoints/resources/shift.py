from flask_restful import Resource, reqparse, abort
from marshmallow_jsonapi.schema import ValidationError

from api.apps.extensions.cache import flask_cache
from api.apps.ponos.middleware.db import PonosDB
from api.apps.ponos.middleware.queue import PonosQueue
from api.apps.ponos.models.cache.shift import ShiftSchema
from api.apps.utilities.endpoints.req_resp import (
    json_api_resp,
    json_api_not_found_resp,
    authenticate_token,
    parse_json_api_data,
    json_api_success
)


class ShiftEndpoints(Resource):
    method_decorators = [authenticate_token]

    def __init__(self):
        self.ponos_db = PonosDB()
        self.ponos_q = PonosQueue()
        self.ponos_serializer = ShiftSchema
        self.request_parser = reqparse.RequestParser()
        super(ShiftEndpoints, self).__init__()

    def __repr__(self):
        return '<{0}> Flask-Restful Resource'.format(self.__class__.__name__)

    @flask_cache.memoize(timeout=50)
    def get(self, shift_id=None):
        """
        Handles HTTP GET requests to /ponos/shift - /ponos/shift/<string:shift_id>
        """

        # Requsting single resource
        if shift_id:

            # Query Mongo database for Shift
            shift = self.ponos_db.get_shift(shift_id=shift_id)

            if shift:
                # Query returned shift. Serialize resource into JSON API specification format.
                resp_json = self.ponos_serializer().dumps(shift).data

                return json_api_resp(resp_json)
            else:
                # Resource not found.
                return json_api_not_found_resp()
        else:
            # Requesting all resources
            # TODO - allowing access to all resources without pageingation can cause a bottleneck.

            # Query Mongo database for all Shifts
            shifts = self.ponos_db.get_all_shifts()

            if shifts:

                # Query returned shifts. Serialize resource into JSON API specification format.
                resp_json = self.ponos_serializer(many=True).dumps(shifts).data

                return json_api_resp(resp_json)
            else:

                # Resources not found.
                return json_api_not_found_resp()

    def post(self, **kwargs):
        """
        Handles HTTP POST requests to /ponos/shift
        """

        try:
            # Parse request
            req_args = parse_json_api_data(self.ponos_serializer())
        except TypeError:
            # Invalid Content-Type header.
            abort(415)
        except (ValueError, ValidationError):
            # Payload invalid JSON or payload failed validation against Shift marshmallow_jsonapi.flask.Schema
            abort(422)

        # Add create shift job to queue
        self.ponos_q.add_create_shift_job(req_args)

        return json_api_success()
