import os
import sys
import unittest

from flask import Flask

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))

from api.apps import create_app


class AppConfigurationTests(unittest.TestCase):
    """
    Test cases for initializing Flask class.
    """

    def test_create_app(self):
        """
        Test configuring Flask isntance.
        """
        dev_app = create_app('develop', 'test')
        self.assertIsInstance(dev_app, Flask)
        self.assertEquals(dev_app.config['ENV'], 'development')

        test_app = create_app('test', 'test')
        self.assertIsInstance(test_app, Flask)
        self.assertEquals(test_app.config['ENV'], 'testing')

        stage_app = create_app('stage', 'test')
        self.assertIsInstance(stage_app, Flask)
        self.assertEquals(stage_app.config['ENV'], 'staging')

        prod_app = create_app('prod', 'test')
        self.assertIsInstance(prod_app, Flask)
        self.assertEquals(prod_app.config['ENV'], 'production')


if __name__ == '__main__':
    unittest.main()