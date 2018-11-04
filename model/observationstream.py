from mongoengine import *
from stream import Stream


class ObservationStream(EmbeddedDocument):
    stream = ReferenceField(Stream, primary_key=True)
    viewer_count = IntField(min_value=0, required=True)
