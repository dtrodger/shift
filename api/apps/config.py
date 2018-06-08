import os

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Set environment variables if configuration.env exists.
config_path = os.path.join(basedir, 'apps/config.env')

# Assert environment configuration file exists
assert os.path.exists(config_path), 'config.env required.'
for line in open(config_path):
    var = line.strip().split('=')
    if len(var) == 2:
        os.environ[var[0]] = var[1].replace("\"", "")


class Config(object):
    """
    Configuration constants to be initialized with Flask object.
    More information - http://flask.pocoo.org/docs/1.0/config/
    """
    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'SECRET_KEY_ENV_VAR_NOT_SET'

    # Custom
    PROJECT = "Shiftgig"
    BASE_DIR = basedir

    # NOT A PRODUCTION STABLE MEANS OF AUTHENTICATING
    API_TOKEN = os.environ.get('SHIFTGIG_API_TOKEN')

    # Flask-SQLAlchemy - TODO Implement JWT Authentication with SQL User Model
    SQLALCHEMY_DATABASE_URI = os.environ.get('SHIFTGIG_SQL_URI') or 'sqlite:///' + os.path.join(basedir, 'data.sqlite')

    # Flask-MongoEngine - http://docs.mongoengine.org/projects/flask-mongoengine/en/latest/
    MONGODB_SETTINGS = {
        'host': os.environ.get('SHIFTGIG_MONGO_HOST') or 'localhost',
        'db': os.environ.get('SHIFTGIG_MONGO_DB') or 'shiftgig',
        'port': int(os.environ.get('SHIFTGIG_MONGO_PORT')) or 27017,
        'username': os.environ.get('SHIFTGIG_MONGO_USERNAME'),
        'password': os.environ.get('SHIFTGIG_MONGO_PASSWORD')
    }

    # Redis - https://redislabs.com/lp/python-redis/
    REDIS_SERVER = os.environ.get('SHIFTGIG_REDIS_SERVER') or 'localhost'
    REDIS_PORT = os.environ.get('SHIFTGIG_REDIS_PORT') or '6379'

    # Flask-Cache - https://pythonhosted.org/Flask-Cache/
    FLASK_CACHE = {
        'CACHE_TYPE': 'redis',
        'HOST': REDIS_SERVER,
        'PORT': REDIS_PORT
    }

    # Boto - http://boto.cloudhackers.com/en/latest/
    AWS_ACCESS_KEY_ID = os.environ.get('SHIFTGIG_AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('SHIFTGIG_AWS_SECRET_ACCESS_KEY')
    AWS_REGION = os.environ.get('SHIFTGIG_AWS_REGION')


class DevelopmentConfig(Config):

    # Flask
    ENV = 'development'
    DEBUG = True

    # Logging - https://docs.python.org/2/library/logging.html
    LOG_FILE = os.path.abspath(os.path.join(Config.BASE_DIR + '/manager/logs/api.log'))

    # Flask-SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # Boto SQS
    SQS_PONOS_Q = os.environ.get('SHIFTGIG_DEV_SQS_PONOS_Q')

    # Boto SNS
    SQS_PONOS_Q_TOPIC = os.environ.get('SHIFTGIG_DEV_SQS_PONOS_Q_TOPIC')


class TestingConfig(Config):

    # Flask
    ENV = 'testing'
    DEBUG = True
    TESTING = True

    # Logging - https://docs.python.org/2/library/logging.html
    LOG_FILE = '/var/log/shift_api/api.log'

    # Flask-SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # Boto SQS
    SQS_PONOS_Q = os.environ.get('SHIFTGIG_TEST_SQS_PONOS_Q')

    # Boto SNS
    SQS_PONOS_Q_TOPIC = os.environ.get('SHIFTGIG_TEST_SQS_PONOS_Q_TOPIC')


class StagingConfig(Config):

    # Flask
    ENV = 'staging'

    # Logging - https://docs.python.org/2/library/logging.html
    LOG_FILE = '/var/log/shift_api/api.log'

    # Flask-SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Boto SQS
    SQS_PONOS_Q = os.environ.get('SHIFTGIG_STAGE_SQS_PONOS_Q')

    # Boto SNS
    SQS_PONOS_Q_TOPIC = os.environ.get('SHIFTGIG_STAGE_SQS_PONOS_Q_TOPIC')

    # Sentry - https://sentry.io/welcome/
    SENTRY_DSN = os.environ.get('SENTRY_DSN')


class ProductionConfig(Config):

    # Flask
    ENV = 'production'

    # Logging - https://docs.python.org/2/library/logging.html
    API_LOG_FILE = '/var/log/shift_api/api.log'
    PONOS_WORKER_LOG_FILE = '/var/log/shift_api/ponos-worker.log'

    # Flask-SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Boto SQS
    SQS_PONOS_Q = os.environ.get('SHIFTGIG_PROD_SQS_PONOS_Q')

    # Boto SNS
    SQS_PONOS_Q_TOPIC = os.environ.get('SHIFTGIG_PROD_SQS_PONOS_Q_TOPIC')

    # Sentry - https://sentry.io/welcome/
    SENTRY_DSN = os.environ.get('SENTRY_DSN')


def options(option):
    """
    Returns requested configuraiton class

    Arguments:
        option (str): str representation of configuration option

    Return:
        (Config)
    """

    # Validate configuration option.
    if option not in ('develop', 'test', 'stage', 'prod'):
        raise NotImplementedError("Invalid configuration choice. Options include ('base', 'develop', 'test', 'prod')")

    # Python switch.
    return {
        'develop': DevelopmentConfig,
        'test': TestingConfig,
        'stage': StagingConfig,
        'prod': ProductionConfig,
    }[option]
