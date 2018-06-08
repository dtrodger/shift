import json
from functools import wraps

from flask import make_response, request, current_app
from flask_restful import reqparse, abort


def json_api_error(status, title, detail=None, source=None, restful_error=None):
    """
    Creates JSON API specification error response payload

    Arguments:
        status (str): HTTP status code
        title (str): Error message content

    Key Word Arguments:
        detail (str): Title detail content
        source (dict): Pointer to endpoint returning error
        restful_error (bool): Determine if error response handled by Flask application of Flask-Resful API

    Return:
        error_resp (str) if not restful_error, else (dict)
    """

    error = {
        'status': status,
        'title': title
    }

    if source:
        error.update({'source': source})
    if detail:
        error.update({'detail': detail})

    error_resp = {'errors': [error]}

    # If error raised by Flask-Restful endpoint, format response accordingly.
    if not restful_error:
        error_resp = json.dumps({'message': error_resp})

    return error_resp


def parse_json_api_data(schema):
    """
    Parses HTTP request Content-Type header and validates it against marshmallow_jsonapi.flask.Schema

    Arguments:
        schema (marshmallow_jsonapi.flask.Schema)

    Return:
        json_api_valid_data (dict): parsed, validated, JSON API resource
    """

    # Parse HTTP request headers.
    parser = reqparse.RequestParser()
    parser.add_argument('Content-Type', location='headers', required=True)
    args = parser.parse_args()
    # Ensure JSON API specification Content-Type value.
    if args.get('Content-Type') != 'application/vnd.api+json':
        raise TypeError
    # Validate parsed data against marshmallow_jsonapi Schema
    parsed_data = json.loads(request.data)
    schema.validate(parsed_data)
    json_api_valid_data = schema.load(parsed_data).data

    return json_api_valid_data


def json_api_resp(json, code=200, headers=None):
    """
    Initialize Flask Response and set HTTP header Content-Type to JSON API specification requirement.

    Arguments:
        json (str): response payload

    Key Word Arguments:
        code (int): HTTP response code
        headers (list): HTTP headers at append to response

    Return:
        (Flask Response)
    """

    resp = make_response(json, code)
    resp.headers['Content-Type'] = 'application/vnd.api+json;charset=utf8'

    if headers:
        resp.headers.extend(headers)

    return resp


def json_api_not_found_resp():
    """
    Personal interpretation on JSON API specification response for no records found.

    Return:
        (Flask Response)
    """

    not_found_json = json.dumps({"data": "record not found"})

    return json_api_resp(not_found_json)


def json_api_success():
    """
    Personal interpretation on JSON API specification response for successfully received and queued payload for
    processing by worker.

    Return:
        (Flask Response)
    """

    success_json = json.dumps({"data": {"message": "success"}})

    return json_api_resp(success_json)


def authenticate_token(fn):
    """
    Parses HTTP request header for Authorization API token.
    TODO - Implement JSON web token authetication with SQL-Alchemy User model. Add logic to this function to validate
    Authorization JSON Web Token.
    """
    @wraps(fn)
    def decorated_function(*args, **kwargs):
        authenticted = False
        parser = reqparse.RequestParser()
        parser.add_argument('Authorization', location='headers', default='')
        req_args = parser.parse_args()
        if req_args['Authorization']:
            token = req_args['Authorization']
            if token == current_app.config.get('API_TOKEN'):
                authenticted = True
            elif token == 'The server is a?':
                abort(418)
        if authenticted:
            return fn(*args, **kwargs)
        else:
            abort(401)
    return decorated_function
