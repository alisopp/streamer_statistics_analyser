from mongoengine import *


class ActualViewerStatistics(EmbeddedDocument):
    observation_date = DateTimeField()
    viewer_count = IntField()