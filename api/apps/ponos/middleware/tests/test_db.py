from itertools import repeat
import os
import sys
import unittest

from flask_testing import TestCase

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))

from api.apps import create_app
from api.apps.ponos.middleware.db import PonosDB
from api.apps.ponos.utilities.mock_data import random_time_slots, mock_shift_data, drop_ponos_collections


# TODO - Add docstrings and comments.


class PonosDBMiddlewareTests(TestCase):

    def create_app(self):
        app = create_app(config='test')
        return app

    def setUp(self):
        self.ponos_db = PonosDB()

    def tearDown(self):
        drop_ponos_collections()

    def test_init_time_slot(self):
        mock_shift_data(self)
        time_slot_start, time_slot_end = random_time_slots()
        time_slot = self.ponos_db.init_time_slot('First', time_slot_start, time_slot_end)
        self.assertIsInstance(time_slot, self.ponos_db.time_slots)

    def test_shift_crud(self):
        #Create
        time_slots = [self.ponos_db.init_time_slot('first', *random_time_slots()) for _ in repeat(None, 3)]
        shift = self.ponos_db.create_shift('1033 W. Loyola', 'Chicago', 'IL', '60626', 'USA', time_slots, description='Test shift description')
        self.assertIsInstance(shift, self.ponos_db.shift)

        q_shift = self.ponos_db.get_first(self.ponos_db.shift, shift_id=shift.shift_id)
        self.assertEquals(shift, q_shift)

        # Read
        q_shift = self.ponos_db.get_shift(shift_id=shift.shift_id)
        self.assertEquals(shift, q_shift)

        # Update
        self.ponos_db.update_shift(q_shift, address='888 Elm Street')
        self.assertEquals(q_shift.address, '888 Elm Street')

        # Delete
        q_shift_id = q_shift.shift_id
        self.ponos_db.delete_shift(shift)
        self.assertEquals(self.ponos_db.get_shift(shift_id=q_shift_id), None)


if __name__ == '__main__':
    unittest.main()

