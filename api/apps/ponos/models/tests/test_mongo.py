from itertools import repeat
import os
import sys
import unittest
import uuid

from flask import current_app
from flask_testing import TestCase

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))

from api.apps import create_app
from api.apps.ponos.models.mongo.shift import (
    Shift,
    TimeSlots
)
from api.apps.ponos.utilities.mock_data import random_time_slots, drop_ponos_collections


# TODO - Add docstrings and comments. Test for failures.


class ShiftMongoTests(TestCase):

    def create_app(self):
        app = create_app(config='test')
        return app

    def setUp(self):
        self.time_slots = TimeSlots
        self.shift = Shift

    def tearDown(self):
        drop_ponos_collections()

    def test_init_time_slot(self):
        time_slot_start, time_slot_end = random_time_slots()
        time_slot = self.time_slots(label='First', start=time_slot_start, end=time_slot_end)
        self.assertIsInstance(time_slot, self.time_slots)

    def test_shift_crud(self):

        # Create
        time_slot_start, time_slot_end = random_time_slots()
        time_slot = self.time_slots(label='First', start=time_slot_start, end=time_slot_end)

        shift = self.shift(shift_id=uuid.uuid4().hex, address='1033 W. Loyola', city='Chicago', state='IL', postal_code='60626', country='USA',
                           time_slots=[time_slot], description='Test shift description')
        shift.save()
        self.assertIsInstance(shift, self.shift)

        # Read
        q_shift = self.shift.objects(shift_id=shift.shift_id).first()
        self.assertEquals(shift, q_shift)

        # Update
        q_shift.address='888 Elm Street'
        q_shift.save()
        self.assertEquals(q_shift.address, '888 Elm Street')

        # Delete
        q_shift_id = q_shift.shift_id
        q_shift.delete()
        self.assertEquals(self.shift.objects(shift_id=q_shift_id).first(), None)



if __name__ == '__main__':
    unittest.main()