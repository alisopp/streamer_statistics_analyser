from mongoengine import *


class Stream(Document):
    stream_id = IntField(required=True)
    user_id = IntField(required=True)
    game_id = IntField()
    observation_time = DateTimeField()
    viewer_count = IntField(min_value=0, required=True)
    meta = {
        'indexes': [
            {'fields': {'stream_id', 'observation_time'}, 'unique': True}
        ]
    }
