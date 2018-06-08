from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Schema


class TimeSlotsSchema(Schema):
    id = fields.String(dump_only=True, attribute='shift_id')
    label = fields.String()
    start = fields.String()
    end = fields.String()

    class Meta:
        type_ = 'time_slots'


class ShiftSchema(Schema):
    id = fields.String(required=True, dump_only=True, attribute='shift_id')
    description = fields.String()
    address = fields.String()
    city = fields.String()
    state = fields.String()
    postal_code = fields.String()
    country = fields.String()
    time_slots = fields.List(fields.Nested(TimeSlotsSchema))
    labels = fields.List(fields.String())

    class Meta:
        type_ = 'shift'
        self_view = 'ponos'
        self_view_many = 'ponos'
        strict = True
