from flask import Flask

from api.apps.config import (
    options,
    Config
)
from api.apps.extensions import initialize_extensions
from api.apps.utilities.errors.error_handlers import register_error_handlers
from api.apps.utilities.endpoints.req_resp import json_api_error


def create_app(config='develop', app_name=Config.PROJECT):
    """
    Flask application factory. Initialize Flask object, configure, and initializes extensions.

    Arguments:
        config (str): Application configuration string representation.
        app_name (str): Application name.

    Return:
        Initialized Flask object.
    """

    config_obj = options(config)
    app = Flask(app_name, static_folder=None)
    app.config.from_object(config_obj)
    initialize_extensions(app)
    register_error_handlers(app)

    return app


__all__ = ['create_app']
