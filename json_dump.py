import codecs
import json
import datetime
import read_streams
import time
from model import *
from model import Streamer, ObservationStream, Observation, Stream


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
    observation = Observation(current_dt)
    for entry in all_data:
        _user_id = entry["user_id"]
        _user_name = entry["user_name"]
        _viewer_count = entry["viewer_count"]
        _stream_id = entry["id"]
        _game_id = entry["game_id"]

        _started_at = entry["started_at"]
        # 2018-11-04T12:02:03Z
        # started_at is in UTC timeformat with a offset of 00:00 hours
        _started_at = datetime.datetime.strptime(_started_at, "%Y-%m-%dT%H:%M:%SZ")
        streamer = Streamer(user_id=_user_id, user_name=_user_name, display_name=_user_name)
        stream = Stream(stream_id=_stream_id, started_at=_started_at, streamer=streamer)
        observation_stream = ObservationStream(viewer_count=_viewer_count, stream=stream)

        if is_int_number(_game_id):
            stream.game_id = _game_id
        streamer.save()
        stream.save()
        observation.streams.append(observation_stream)
    observation.save()
    print("Fetched data waiting now 5 min for next data")
    time.sleep(300)
