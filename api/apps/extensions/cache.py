from redis import StrictRedis
from flask_cache import Cache


class RedisCache(object):

    def __init__(self, strict_redis_api=None):
        self.api = strict_redis_api

    def init_app(self, app, host=None, port=None, db=0):
        """
        Initializes a Redis clients with custom or Flask application configuration.

        Arguments:
             app (Flask instace):
             host (str): Redis host server
             port (str): Redis host server port
             db (int): Redis host server db

        Returns:
            self.api (StrictRedis instance):
        """

        # If no host or port are provided, connect to client with Flask application configuration.
        if host is None:
            host = app.config['REDIS_SERVER']
        if port is None:
            port = app.config['REDIS_PORT']

        try:
            # Initialize Redis client. Set as instance attribute.
            self.api = StrictRedis(host=host, port=port, db=db)
            return self.api
        except Exception as err:
            raise err

    def get_api(self):
        """
        Getter for Redis client
        Returns:
            self.api (StrictRedis instance):
        """
        return self.api


# py-redis - http://redis-py.readthedocs.io/en/latest/
redis_cache = RedisCache()

# Flask-Cache - https://pythonhosted.org/Flask-Cache/
flask_cache = Cache()
