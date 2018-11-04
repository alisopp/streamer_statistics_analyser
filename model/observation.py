from mongoengine import *
from observationstream import ObservationStream


class Observation(Document):
    observation_time = DateTimeField(primary_key=True)
    streams = ListField(EmbeddedDocumentField(ObservationStream))
