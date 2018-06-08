import unittest

from flask import current_app


def cli_test_app_config():
    """
    Finds and runs Flask application configuration tests.
    """
    current_app.logger.info('Running application configuration tests.')

    # Find tests.
    tests = unittest.TestLoader().discover('apps.tests')

    # Run rests.
    unittest.TextTestRunner().run(tests)