from itertools import repeat
import os
import sys
import unittest

from flask_testing import TestCase

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))

from api.apps import create_app
from api.apps.ponos.middleware.queue import PonosQueue


# TODO - Add docstrings and comments.


class PonosQueueMiddlewareTests(TestCase):

    def create_app(self):
        app = create_app(config='test')
        return app

    def test_init_queue(self):
        ponos_queue = PonosQueue()


if __name__ == '__main__':
    unittest.main()