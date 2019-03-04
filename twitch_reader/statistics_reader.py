import datetime
from mongoengine import *

import json_dump
from model import Streamer, StreamMetaData, db_initializer, CalculatedStatistics
import settings

colors = [  # from https://sashat.me/2017/01/11/list-of-20-simple-distinct-colors/
    "#e6194b", "#3cb44b", "#ffe119", "#0082c8", "#f58231", "#911eb4", "#46f0f0", "#f032e6",
    "#d2f53c", "#fabebe", "#008080", "#e6beff", "#aa6e28", "#fffac8", "#800000", "#aaffc3",
    "#808000", "#ffd8b1", "#000080", "#808080", "#000000"
]


def get_streamers_with_the_most_viewers(limit):
    result_list = []
    for result in Streamer.objects.order_by('-highest_viewer_count').limit(limit):
        result_list.append(result.user_name)
    return result_list


def get_stream_data_for_user(streamer_id, start_date, end_date):
    start_of_start_date = datetime.datetime(start_date.year, start_date.month, start_date.day, 0, 0, 00)
    end_of_end_date = datetime.datetime(end_date.year, end_date.month, end_date.day, 23, 59, 59)
    streams = StreamMetaData.objects(streamer=streamer_id).filter(
        Q(viewer_counts__observation_date__gte=start_of_start_date) &
        Q(viewer_counts__observation_date__lte=end_of_end_date))
    return streams


def get_data_per_language(start_date, end_date, title_pre, languages):
    title = title_pre.join(languages) + start_date.strftime("%Y.%m.%d") + " - " + end_date.strftime("%Y.%m.%d")
    cached_result = CalculatedStatistics.objects(title_sub=title).first()
    if cached_result is not None:
        json_dict = {}
        for field in cached_result:
            if "id".__eq__(field):
                continue
            json_dict[field] = cached_result[field]
        return json_dict
    pipeline = [
        {"$addFields": {
            "stream_start": {"$arrayElemAt": ["$viewer_counts", 0]},
            "stream_end": {"$arrayElemAt": ["$viewer_counts", -1]}
        }},
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
    ]
    if languages.__len__() > 0:
        pipeline.insert(0, {"$match": {"language": {"$in": languages}}})
    streams_per_language = StreamMetaData.objects.aggregate(*pipeline)
    time_set = set()
    data_per_language = list()
    for lang_stream in streams_per_language:
        data_per_language.append(lang_stream)
        language_times = lang_stream["observations"]
        for x in language_times:
            time_set.add(x)
    time_set = sorted(time_set)
    return create_chart_js(time_set, data_per_language, title)


def create_chart_js(time_set, data_per_language, title):
    current_color = 0
    json_dict = {'chart_data': []}
    for lang_stream in data_per_language:

        chart_data = lang_stream["chart_data"]
        chart_data['fill'] = False
        chart_data['backgroundColor'] = colors[current_color]
        chart_data['borderColor'] = colors[current_color]
        language_times = lang_stream["observations"]

        for x in range(0, time_set.__len__()):
            saved_times_of_current_set = x
            if saved_times_of_current_set >= language_times.__len__():
                saved_times_of_current_set = language_times.__len__() - 1
            saved_time = time_set[x]
            time_to_check = language_times[saved_times_of_current_set]
            if saved_time > time_to_check:
                chart_data['data'].insert(saved_times_of_current_set, 0)
                language_times.insert(saved_times_of_current_set + 1, saved_time)
            elif saved_time < time_to_check:
                chart_data['data'].insert(saved_times_of_current_set, 0)
                language_times.insert(saved_times_of_current_set, saved_time)
        current_color = (current_color + 1) % colors.__len__()
        json_dict['chart_data'].append(chart_data)
    for i in range(0, time_set.__len__()):
        time_set[i] = time_set[i].strftime("%Y-%m-%d %H:%M")
    json_dict["observation_date"] = time_set
    json_dict["title_sub"] = title
    statistic = CalculatedStatistics(title_sub=title, observation_date=time_set, chart_data=json_dict["chart_data"])
    statistic.save()
    # db = db_initializer.DbConnector.getInstance().db_client[settings.env_variables.db_name]
    # mycol = db[settings.env_variables.cache_col_name]
    # mycol.insert_one(json_dict)
    return json_dict


def get_streamer_data(start_date, end_date, title_pre, streamers):
    if streamers.__len__() == 0:
        streamers = get_streamers_with_the_most_viewers(10)
    title = title_pre + "".join(streamers) + start_date.strftime("%Y.%m.%d") + " - " + end_date.strftime("%Y.%m.%d")
    cached_result = CalculatedStatistics.objects(title_sub=title).first()
    if cached_result is not None:
        json_dict = {}
        for field in cached_result:
            if "id".__eq__(field):
                continue
            json_dict[field] = cached_result[field]
        return json_dict
    streamers = Streamer.objects.aggregate(
        {"$match": {"user_name": {"$in": streamers}}},
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
        {"$project": {"observations": "$observation_date", "chart_data.data": "$viewer_count",
                      "chart_data.label": "$display_name"}}
    )
    time_set = set()
    data_per_streamer = list()
    for lang_stream in streamers:
        data_per_streamer.append(lang_stream)
        streamer_times = lang_stream["observations"]
        for x in streamer_times:
            time_set.add(x)
    time_set = sorted(time_set)
    return create_chart_js(time_set, data_per_streamer, title)
