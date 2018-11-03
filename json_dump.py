import codecs
import json
import datetime
import read_streams
import time
from model import *
from model import Streamer, Stream, Date


def is_int_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


while True:
    current_dt = datetime.datetime.utcnow()

    with codecs.open("streams_" + str(current_dt).replace(" ", "_").replace(":", "_") + ".json", "w", "utf-8") as file:
        all_data = read_streams.read_twitch_streams()
        date = Date(current_dt)
        for entry in all_data:
            _user_id = entry["user_id"]
            _user_name = entry["user_name"]
            _viewer_count = entry["viewer_count"]
            _stream_id = entry["id"]
            _game_id = entry["game_id"]
            streamer = Streamer(user_id=_user_id, user_name=_user_name, display_name=_user_name)
            stream = Stream(stream_id=_stream_id, user_id=_user_id,
                            viewer_count=_viewer_count)

            if is_int_number(_game_id):
                stream.game_id = _game_id
            streamer.save()

            date.streams.append(stream)
        date.save()
        # closing file
        json.dump(all_data, file)
        file.close()
        print("Fetched data waiting now 5 min for next data")
        time.sleep(300)

