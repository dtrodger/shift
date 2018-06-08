import uuid

from flask import current_app

from api.apps.ponos.models.mongo.shift import (
    Shift,
    TimeSlots
)
from api.apps.utilities.middleware.mongo.crud import MongoCRUD


# TODO - Add docstrings and comments.

class PonosDB(MongoCRUD):

    def __init__(self):
        self.shift = Shift
        self.time_slots = TimeSlots
        self.log = current_app.logger

    @classmethod
    def generate_id(cls):
        return uuid.uuid4().hex

    def create_shift(self, address, city, state, postal_code, country, time_slots, **kwargs):
        shift_id = self.generate_id()
        new_shift = self.create(self.shift, shift_id=shift_id, address=address, city=city, state=state,
                                postal_code=postal_code, country=country, time_slots=time_slots, **kwargs)

        return new_shift

    def get_shift(self, **kwargs):
        return self.get_first(self.shift, **kwargs)

    def get_all_shifts(self, **kwargs):
        return self.get_all(self.shift, **kwargs)

    def get_time_slots(self, **kwargs):
        return self.get_first(self.time_slots, **kwargs)

    def get_all_time_slots(self, **kwargs):
        return self.get_all(self.time_slots, **kwargs)

    def update_shift(self, shift, **kwargs):
        if isinstance(shift, self.shift):
            return self.update(shift, **kwargs)
        else:
            raise TypeError('Shift MongoEngine instance required as arg')

    def delete_shift(self, shift):
        if isinstance(shift, self.shift):
            return self.delete(shift)
        else:
            raise TypeError('Shift MongoEngine instance required as arg')

    def init_time_slot(self, label, start, end):
        new_time_slot = self.time_slots(label=label, start=start, end=end)
        return new_time_slot

    def create_shift_job(self, json_api_data):
        time_slots = [self.init_time_slot(time_slot['label'], time_slot['start'], time_slot['end']) for time_slot in
                      json_api_data.get('time_slots')]

        return self.create_shift(json_api_data['address'], json_api_data['city'], json_api_data['state'],
                                 json_api_data['postal_code'], json_api_data['country'], time_slots,
                                 labels=json_api_data.get('labels'))

