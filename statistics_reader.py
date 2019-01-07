import datetime
import json_dump
import matplotlib.pyplot as plt
from matplotlib import dates
from mongoengine import *

from model import Streamer, StreamMetaData

colors = [  # from https://sashat.me/2017/01/11/list-of-20-simple-distinct-colors/
    "#e6194b", "#3cb44b", "#ffe119", "#0082c8", "#f58231", "#911eb4", "#46f0f0", "#f032e6",
    "#d2f53c", "#fabebe", "#008080", "#e6beff", "#aa6e28", "#fffac8", "#800000", "#aaffc3",
    "#808000", "#ffd8b1", "#000080", "#808080", "#FFFFFF", "#000000"
]


def get_streamers_with_the_most_viewers(limit):
    return Streamer.objects.order_by('-highest_viewer_count').limit(limit)


def get_stream_data_for_user(streamer_id, start_date, end_date):
    start_of_start_date = datetime.datetime(start_date.year, start_date.month, start_date.day, 0, 0, 00)
    end_of_end_date = datetime.datetime(end_date.year, end_date.month, end_date.day, 23, 59, 59)
    streams = StreamMetaData.objects(streamer=streamer_id).filter(
        Q(viewer_counts__observation_date__gte=start_of_start_date) &
        Q(viewer_counts__observation_date__lte=end_of_end_date))
    return streams


def get_data(streams):
    cnt = 0
    x = []  # rank
    y = []  # viewer count
    s = []  # seconds running
    game_id = 0
    for stream in streams:
        game_id = stream.game_id
        for entry in stream.viewer_counts:
            date_tmp = str(entry.observation_date)
            # td = parser.parse(str(entry.observation_date)) - datetime.datetime(1970, 1, 1)
            cnt = cnt + 1
            x.append(cnt)
            y.append(entry.viewer_count)
            s.append(dates.datestr2num(date_tmp))
            # s.append(td)
    return (x, y, s, game_id)


def get_data_per_language(start_date, end_date):
    streams_per_language = StreamMetaData.objects.aggregate(
        {"$unwind": "$viewer_counts"},

        {"$match":
            {"$expr":
                {"$and":
                    [
                        {"$gte": ["$viewer_counts.observation_date", start_date]},
                        {"$lte": ["$viewer_counts.observation_date", end_date]}
                    ]
                }
            }
        },
        {"$project": {"viewer_count": "$viewer_counts.viewer_count", "language": 1,
                      "observation_date": "$viewer_counts.observation_date"}},
        {"$group": {"_id": {"language": "$language", "observation_date": "$observation_date"},
                    "viewer_count": {"$sum": "$viewer_count"}}},
        {"$sort": {"_id.observation_date": 1}},
        {"$group": {"_id": "$_id.language", "observations": {"$push": "$_id.observation_date"},
                    "data": {"$push": "$viewer_count"}}},
        {"$project": {"chart_data.label": "$_id", "observations": 1, "chart_data.data": "$data"}}
        # create chart js

    )
    current_color = 0
    amount_of_times_in_last_set = 0
    json_dict = {}
    json_dict['chart_data'] = []
    observation_times = []
    time_set = set()
    data_per_language = list()
    for lang_stream in streams_per_language:
        data_per_language.append(lang_stream)
        language_times = lang_stream["observations"]
        for x in language_times:
            time_set.add(x)
    time_set = sorted(time_set)
    for lang_stream in data_per_language:

        chart_data = lang_stream["chart_data"]
        chart_data['fill'] = False
        chart_data['backgroundColor'] = colors[current_color]
        chart_data['borderColor'] = colors[current_color]
        language_times = lang_stream["observations"]
        current_amount_of_times = language_times.__len__()

        for x in (0, time_set.__len__() - 1):
            saved_times_of_current_set = x
            if saved_times_of_current_set >= current_amount_of_times:
                saved_times_of_current_set = current_amount_of_times - 1
            saved_time = time_set[x]
            time_to_check = language_times[saved_times_of_current_set]
            if saved_time > time_to_check:
                chart_data['data'].insert(saved_times_of_current_set, 0)
                language_times.insert(saved_times_of_current_set + 1, saved_time)
            elif saved_time < time_to_check:
                chart_data['data'].insert(saved_times_of_current_set, 0)
                language_times.insert(saved_times_of_current_set, saved_time)
        print "language " + chart_data["label"]
        current_color = (current_color + 1) % colors.__len__()
        json_dict['chart_data'].append(chart_data)

    json_dict["observation_date"] = time_set
    json_dict["title_sub"] = start_date.strftime("%Y.%m.%d") + " - " + end_date.strftime("%Y.%m.%d")
    json_dump.single_array_save(json_dict, "html/data")


def get_data_for_chart_js(streamer, start_date, end_date):
    streamers = Streamer.objects.aggregate(
        {"$match": {"user_name": {"$in": streamer}}},
        {"$lookup":
            {
                "from": "stream_meta_data",
                "let": {"streamer": "$_id"},
                "pipeline": [{"$match":
                    {"$expr":
                        {"$and":
                            [
                                {"$eq": ["$streamer_id", "$$streamer"]},
                            ]
                        }
                    }
                },
                    {"$group": {"_id": "$streamer_id", "items": {"$push": "$viewer_counts"}}},
                    {"$unwind": "$items"},
                    {"$unwind": "$items"},
                    {"$match": {"$expr":
                        {"$and":
                            [
                                {"$gte": ["$items.observation_date", start_date]},
                                {"$lte": ["$items.observation_date", end_date]}
                            ]
                        }
                    }},
                    {"$group": {"_id": "$_id", "observations": {"$push": "$items"}}},
                    {"$project": {"viewer_count": "$observations.viewer_count",
                                  "observation_date": "$observations.observation_date",
                                  "display_name": "$display_name"}}
                    ,
                ],
                "as": "streams"
            }

        },
        {"$project": {"viewer_count": "$streams.viewer_count",
                      "observation_date": "$streams.observation_date", "display_name": "$display_name"}},
        {"$unwind": "$viewer_count"},
        {"$unwind": "$observation_date"},
        {"$project": {"observation_date": "$observation_date", "chart_data.data": "$viewer_count",
                      "chart_data.label": "$display_name"}}
    )
    return streamers


def createStreamerData():
    streamerList = get_data_for_chart_js(["Ninja", "TimTheTatman"], datetime.datetime(2018, 11, 5, 18, 0, 28, 324000),
                                         datetime.datetime(2018, 11, 25, 19, 14, 28, 324000))

    currentColor = 0
    json_dict = {}
    json_dict['chart_data'] = []
    for streamer in streamerList:
        chart_data = streamer["chart_data"]
        chart_data['fill'] = False
        chart_data['backgroundColor'] = colors[currentColor]
        chart_data['borderColor'] = colors[currentColor]
        currentColor += 1
        observation_times = streamer["observation_date"]
        json_dict['chart_data'].append(chart_data)
        json_dict['observation_date'] = observation_times

    json_dump.single_array_save(json_dict, "html/data")


get_data_per_language(datetime.datetime(2018, 10, 29, 0, 0, 0, 0),
                      datetime.datetime(2018, 11, 5, 0, 0, 0, 0))
