from mongoengine import *

from twitch_statistics_reader.model import Streamer, ActualViewerStatistics


class StreamMetaData(Document):
    stream_id = IntField(primary_key=True)
    streamer_id = ReferenceField(Streamer)
    game_id = IntField()
    started_at = DateTimeField()
    language = StringField()
    title = StringField()
    viewer_counts = ListField(EmbeddedDocumentField(ActualViewerStatistics))
    last_record = DateTimeField()
