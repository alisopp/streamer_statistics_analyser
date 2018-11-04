from mongoengine import *
from streamer import Streamer


class Stream(Document):
    stream_id = IntField(primary_key=True)
    streamer = ReferenceField(Streamer)
    game_id = IntField()
    started_at = DateTimeField()
