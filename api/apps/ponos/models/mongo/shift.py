from datetime import datetime

from api.apps.extensions import mongodb


class TimeSlots(mongodb.EmbeddedDocument):
    label = mongodb.StringField()
    start = mongodb.DateTimeField(required=True)
    end = mongodb.DateTimeField(required=True)


class Shift(mongodb.Document):
    shift_id = mongodb.UUIDField(required=True, unique=False)
    description = mongodb.StringField()
    address = mongodb.StringField(required=True)
    city = mongodb.StringField(required=True)
    state = mongodb.StringField(required=True)
    postal_code = mongodb.StringField(required=True)
    country = mongodb.StringField(required=True)
    time_slots = mongodb.EmbeddedDocumentListField(TimeSlots)
    labels = mongodb.ListField(mongodb.StringField())
    created_dt = mongodb.DateTimeField(default=datetime.now())
    updated_dt = mongodb.DateTimeField(default=datetime.now())

    # Allow document to be inherited for dynamic models.
    meta = {
        'allow_inheritance': True
    }

# def update_modified(sender, document):
#     document.updated_dt = datetime.utcnow()
#
# signals.pre_save.connect(update_modified)
