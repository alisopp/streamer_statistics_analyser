from mongoengine import *
from stream import Stream


class Date(Document):
    observation_time = DateTimeField(primary_key=True)
    streams = ListField(EmbeddedDocumentField(Stream))
