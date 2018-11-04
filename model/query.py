import datetime
from mongoengine import *
from model import *
from model import Streamer, db_client


def get_viewer_results_per_day(streamer, date):
    start_of_day = datetime.datetime(date.year, date.month, date.day, 0, 0, 00)
    end_of_day = datetime.datetime(date.year, date.month, date.day, 23, 59, 59)
    streamer = Streamer.objects(user_name=streamer).filter(Q(viewer__observation_date__gte=start_of_day) &
                                                           Q(
                                                               viewer__observation_date__lte=end_of_day))
    streamer = streamer.first()
    return streamer

def update_highest_viewer_results():
    streamers = Streamer.objects()

    for streamer in streamers:
        highest_viewer_count = 0
        date = datetime.datetime.utcnow()
        for view in streamer.viewer:
            if view.viewer_count >= highest_viewer_count:
                highest_viewer_count = view.viewer_count
                date = view.observation_date
        streamer.datetime_of_the_highest_viewer_count = date
        streamer.highest_viewer_count = highest_viewer_count
        streamer.save()

