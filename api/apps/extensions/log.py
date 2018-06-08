import logging
from logging.handlers import RotatingFileHandler


def configure_logging(app):
    """
    Utility function to set Flask instance logging with configuration context specific levels.

    Arguments:
        app (Flask instance):

    Returns:
        (None)
    """
    # pass
    # Set base logging config based on Flask application debug mode.
    if app.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.ERROR)

    # Initialize file handler at Flask application config log file location.
    file_handler = RotatingFileHandler(app.config['LOG_FILE'], maxBytes=1000, backupCount=0)

    file_handler.setFormatter(
        logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'
        )
    )

    console = logging.StreamHandler()

    if app.debug:
        file_handler.setLevel(logging.DEBUG)
        console.setLevel(logging.DEBUG)
    else:
        file_handler.setLevel(logging.ERROR)
        console.setLevel(logging.ERROR)

    # Add file handler to Flask application and various extensions.
    # TODO - configure for all extensions.
    app.logger.addHandler(file_handler)

    faker_logger = logging.getLogger('faker.factory')
    faker_logger.setLevel(logging.INFO)

    redis_logger = logging.getLogger('redis')
    redis_logger.setLevel(logging.INFO)
    redis_logger.addHandler(file_handler)

    mongoengine_logger = logging.getLogger('mongoengine')
    mongoengine_logger.setLevel(logging.INFO)
    mongoengine_logger.addHandler(file_handler)

    sqlalchemy_logger = logging.getLogger('sqlalchemy')
    sqlalchemy_logger.setLevel(logging.INFO)
    sqlalchemy_logger.addHandler(file_handler)

    boto_logger = logging.getLogger('boto')
    boto_logger.setLevel(logging.INFO)
    boto_logger.addHandler(file_handler)
