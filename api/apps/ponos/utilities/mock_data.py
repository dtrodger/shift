import datetime
from itertools import repeat
import random

from faker import Faker

from api.apps.ponos.middleware.db import PonosDB


def random_time_slots():
    """
    Creates random datetime obects for mocking MongoEngine TimeSlot instances.

    Return:
        (datetime, datetime)
    """

    end = datetime.datetime.now() - datetime.timedelta(days=random.randint(1, 100))
    start = end - datetime.timedelta(hours=random.randint(1, 8))
    return start, end


def mock_shift_data(self=None):
    """
    Saves mock MongoEngine Shifts to Mongo.

    Key Word Argument:
        self (TestCase): sets instance attribute of all shifts to TestCase instance if being called within unit test
        setUp method.

    Return:
        (datetime, datetime)
    """

    # Initialize helper APIs.
    ponos_db = PonosDB()
    fake = Faker()

    # Assign shifts to TestCase instance attribute for reference in unit tests.
    if self:
        self.shifts = []

    for _ in repeat(None, 10):

        # Initialize MongoEngine TimeSlots.
        time_slots = [ponos_db.init_time_slot(fake.word(), *random_time_slots()) for _ in repeat(None, random.randint(1, 10))]
        labels = [fake.word() for _ in repeat(None, random.randint(1, 10))]

        # Initialize and save MongoEngine Shift to database.
        shift = ponos_db.create_shift(fake.address(), fake.city(), fake.state(), fake.zipcode(), fake.country(),
                                      time_slots, description=fake.text(), labels=labels)

        # Assign shifts to TestCase instance attribute for reference in unit tests.
        if self:
            self.shifts.append(shift)


def drop_ponos_collections():
    """
    Drops all Ponos DB collections.
    """

    ponos_db = PonosDB()
    ponos_db.drop_collection(ponos_db.shift)
