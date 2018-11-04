from mongoengine import *


class Viewer(EmbeddedDocument):
    observation_date = DateTimeField()
    viewer_count = IntField()