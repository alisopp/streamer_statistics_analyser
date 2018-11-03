from mongoengine import *


class Stream(EmbeddedDocument):

    stream_id = IntField(primary_key=True)
    user_id = IntField(required=True)

    game_id = IntField()

    viewer_count = IntField(min_value=0, required=True)


