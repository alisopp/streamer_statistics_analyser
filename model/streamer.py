from mongoengine import *

class Streamer(Document):
    user_id = IntField(required=True, primary_key=True)
    user_name = StringField(required=True,max_length=50, unique=True)
    display_name = StringField(required=False,max_length=50)
