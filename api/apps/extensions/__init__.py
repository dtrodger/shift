from api.apps.extensions.cache import (
    flask_cache,
    redis_cache
)
from api.apps.extensions.log import configure_logging
from api.apps.extensions.mongoengine import mongodb
from api.apps.extensions.rest import rest_api
from api.apps.ponos.endpoints.register_endpoints import register_ponos_endpoints


def initialize_extensions(app):

    # Logging
    configure_logging(app)

    # Mongo Engine
    mongodb.init_app(app)

    # Flask-Restful
    endpoint_registries = [register_ponos_endpoints]
    rest_api.init_app(app, endpoint_registries)

    # Redis-Cache
    redis_cache.init_app(app)

    # Flask-Cache
    flask_cache.init_app(app, config=app.config['FLASK_CACHE'])

    if app.config['ENV'] == 'production' and app.name != 'test':

        # Flask-SSLify
        from api.apps.extensions.ssl import SSLify
        SSLify(app)

        # Sentry
        from api.apps.extensions.sentry import Sentry
        Sentry(app, dsn=app.config['SENTRY_DSN'])

    return app
