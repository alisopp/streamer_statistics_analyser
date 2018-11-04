from mongoengine import *

from model import Viewer


class Streamer(Document):
    user_id = IntField(required=True, primary_key=True)
    user_name = StringField(required=True, max_length=50, unique=True)
    display_name = StringField(required=False, max_length=50)
    highest_viewer_count = IntField()
    datetime_of_the_highest_viewer_count = DateTimeField()
    last_record = DateTimeField()

    viewer = ListField(EmbeddedDocumentField(Viewer))