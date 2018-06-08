from flask_restful import Api

from api.apps.utilities.endpoints.req_resp import json_api_error

# Define custom HTTP error response payload. Overides default messages from werkzeug.exceptions
errors = {
    'BadRequest': {
        'message': json_api_error('401', 'Client error', restful_error=True),
    },
    'Unauthorized': {
        'message': json_api_error('401', 'Unauthorized', restful_error=True),
    },
    'Forbidden': {
        'message': json_api_error('403', 'Forbidden', restful_error=True),
    },
    'NotFound': {
        'message': json_api_error('404', 'Not found', restful_error=True),
    },
    'UnsupportedMediaType': {
        'message': json_api_error('415', 'Content-Type Header application/vnd.api+json required', restful_error=True),
    },
    'ImATeapot': {
        'message': json_api_error('418', 'This server is a teapot, not a coffee machine', restful_error=True),
    },
    'UnprocessableEntity': {
        'message': json_api_error('422', 'Improper JSON API request. See http://jsonapi.org/.', restful_error=True),
    },
    'InternalServerError': {
        'message': json_api_error('500', 'Internal server error', restful_error=True),
    },
}


class FlaskRestApi(object):
    """
    Utility to mimic Flask Extension.init_app pattern while configuring customer error messages.
    """

    def __init__(self):
        self.api = Api

    def init_app(self, app, endpoint_registries):
        """
        Initializes Flask-Restful API class with Flask application context, configures custom error messages
        and registers API endpoints.

        Arguments:
             app (Flask instace)

        Return:
            None
        """

        # Initialize Flask-Restful instance with Flask application context and custom errors.
        rest_api = self.api(app, errors=errors)

        [endpoint_registry(rest_api) for endpoint_registry in endpoint_registries]

rest_api = FlaskRestApi()
