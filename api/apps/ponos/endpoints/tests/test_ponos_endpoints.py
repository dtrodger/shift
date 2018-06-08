import json
import os
import sys
import unittest

from flask import current_app, url_for
from flask_testing import TestCase

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../../')))

from api.apps import create_app
from api.apps.ponos.utilities.mock_data import mock_shift_data, drop_ponos_collections
from api.apps.ponos.models.cache.shift import ShiftSchema
from api.apps.ponos.middleware.db import PonosDB
from api.apps.ponos.middleware.queue import PonosQueue
from api.apps.ponos.endpoints.tests.mock_data.post_ponos import payload_1


# TODO - Add docstrings and comments. Test for failures.


class PonosShiftEndpointTests(TestCase):

    def create_app(self):
        app = create_app(config='test')
        return app

    def setUp(self):
        self.ponos_db = PonosDB()
        self.ponos_q = PonosQueue()
        self.ponos_serializer = ShiftSchema
        self.headers = {
            'Content-Type': 'application/vnd.api+json',
            'Accept': 'application/vnd.api+json',
            'Authorization': current_app.config['API_TOKEN']
        }
        mock_shift_data(self)

    def tearDown(self):
        drop_ponos_collections()

    def _test_get_id_shift(self):
        shift_id = self.shifts[0].shift_id
        resp = self.client.get(url_for('ponos', shift_id=shift_id), headers=self.headers)
        self.assert200(resp)

        test_shift = self.ponos_db.get_first(self.ponos_db.shift, shift_id=shift_id)
        self.assertEqual(resp.data, self.ponos_serializer().dumps(test_shift).data)

    def _test_get_all_shift(self):
        resp = self.client.get(url_for('ponos'), headers=self.headers)
        self.assert200(resp)

        test_shifts = self.ponos_db.get_all(self.ponos_db.shift)
        self.assertEqual(resp.data, self.ponos_serializer(many=True).dumps(test_shifts).data)

    def test_post_shift(self):
        resp = self.client.post(url_for('ponos'), data=json.dumps(payload_1), headers=self.headers)
        self.assert200(resp)
        # TODO - Test more cases





if __name__ == '__main__':
    unittest.main()
