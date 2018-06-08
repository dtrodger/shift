from api.apps.ponos.endpoints.resources.shift import ShiftEndpoints


def register_ponos_endpoints(rest_api):
    """
    Registers Flask-Restful Resource class on Flask-Restful Api instance.

    Argument:
        rest_api (Flask-Restful Api instance)
    """

    rest_api.add_resource(
        ShiftEndpoints,
        '/ponos/shift',
        '/ponos/shift/<string:shift_id>',
        endpoint='ponos'
    )
