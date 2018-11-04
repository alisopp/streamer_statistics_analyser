import codecs
import json
import datetime
import read_streams
import time
from model import *
from model import Streamer, Viewer


def is_int_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


while True:
    current_dt = datetime.datetime.utcnow()
    print("Start reading data")
    all_data = read_streams.read_twitch_streams(20)
    print("Saving data")
    for entry in all_data:
        _user_id = entry["user_id"]
        _user_name = entry["user_name"]
        _viewer_count = entry["viewer_count"]

        # 2018-11-04T12:02:03Z
        # started_at is in UTC timeformat with a offset of 00:00 hours
        # _started_at = datetime.datetime.strptime(_started_at, "%Y-%m-%dT%H:%M:%SZ")
        streamer = Streamer.objects(user_id=_user_id).first()
        if streamer is None:
            streamer = Streamer(user_id=_user_id, user_name=_user_name, display_name=_user_name)
        else:
            if streamer.highest_viewer_count <= _viewer_count:
                streamer.highest_viewer_count = _viewer_count
                streamer.datetime_of_the_highest_viewer_count = current_dt
        streamer.last_record = current_dt
        viewer = Viewer(viewer_count=_viewer_count, observation_date=current_dt)
        streamer.viewer.append(viewer)
        streamer.save()

    print("Fetched data waiting now 5 min for next data")
    time.sleep(300)
