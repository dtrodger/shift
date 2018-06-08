import unittest

from flask import current_app


def cli_test_ponos_endpoints():
    """
    CLI command function for running Ponos model tests.
    """

    current_app.logger.info('Running Ponos models tests.')
    tests = unittest.TestLoader().discover('apps.ponos.models.tests')
    unittest.TextTestRunner().run(tests)


def cli_test_ponos_middleware():
    """
    CLI command function for running Ponos middleware tests.
    """

    current_app.logger.info('Running Ponos middleware tests.')
    tests = unittest.TestLoader().discover('apps.ponos.middleware.tests')
    unittest.TextTestRunner().run(tests)


def cli_test_ponos_models():
    """
    CLI command function for running Ponos endpoint tests.
    """

    current_app.logger.info('Running Ponos endpoints tests.')
    tests = unittest.TestLoader().discover('apps.ponos.endpoints.tests')
    unittest.TextTestRunner().run(tests)


def cli_test_ponos():
    """
    CLI command function for running all Ponos.
    """

    current_app.logger.info('Running Ponos tests.')
    cli_test_ponos_models()
    cli_test_ponos_middleware()
    cli_test_ponos_endpoints()
