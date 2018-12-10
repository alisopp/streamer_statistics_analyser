import datetime

from model import Streamer, ActualViewerStatistics, StreamMetaData


def is_int_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def save_into_database(all_data, current_dt):
    for entry in all_data:
        _user_id = entry["user_id"]
        _user_name = entry["user_name"]
        _viewer_count = entry["viewer_count"]
        _stream_id = entry["id"]
        _stream_title = entry["title"]
        _language = entry["language"]
        _started_at = entry["started_at"]
        _community_ids = entry["community_ids"]
        _game_id = entry["game_id"]
        _started_at = datetime.datetime.strptime(_started_at, "%Y-%m-%dT%H:%M:%SZ")

        # 2018-11-04T12:02:03Z
        # started_at is in UTC timeformat with a offset of 00:00 hours
        # _started_at = datetime.datetime.strptime(_started_at, "%Y-%m-%dT%H:%M:%SZ")
        streamer = Streamer.objects(user_id=_user_id).first()
        if streamer is None:
            streamer = Streamer(user_id=_user_id, user_name=_user_name, display_name=_user_name)
            streamer.highest_viewer_count = _viewer_count
            streamer.datetime_of_the_highest_viewer_count = current_dt
        else:
            if streamer.highest_viewer_count <= _viewer_count:
                streamer.highest_viewer_count = _viewer_count
                streamer.datetime_of_the_highest_viewer_count = current_dt
        streamer.last_record = current_dt
        stream = StreamMetaData.objects(stream_id=_stream_id).first()
        if stream is None:
            stream = StreamMetaData(stream_id=_stream_id, title=_stream_title, language=_language,
                                    started_at=_started_at, streamer_id=streamer)
        if is_int_number(_game_id):
            _game_id = int(_game_id)
            stream.game_id = _game_id
        viewer = ActualViewerStatistics(viewer_count=_viewer_count, observation_date=current_dt)
        stream.viewer_counts.append(viewer)
        stream.save()
        streamer.save()
