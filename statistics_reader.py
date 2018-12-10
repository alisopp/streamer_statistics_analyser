import datetime
import json_dump
import matplotlib.pyplot as plt
from matplotlib import dates
from mongoengine import *

from model import Streamer, StreamMetaData


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


streamerList = get_data_for_chart_js(["Ninja", "TimTheTatman"], datetime.datetime(2018, 11, 5, 18, 0, 28, 324000),
                                     datetime.datetime(2018, 11, 5, 19, 14, 28, 324000))
colors = [  # from https://sashat.me/2017/01/11/list-of-20-simple-distinct-colors/
    "#e6194b", "#3cb44b", "#ffe119", "#0082c8", "#f58231", "#911eb4", "#46f0f0", "#f032e6",
    "#d2f53c", "#fabebe", "#008080", "#e6beff", "#aa6e28", "#fffac8", "#800000", "#aaffc3",
    "#808000", "#ffd8b1", "#000080", "#808080", "#FFFFFF", "#000000"
]
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
""" 
"localField" : "_id",
"foreignField" : "streamer",
"allValues": { "$setUnion": [ "$A", "$B" ] }
startDate = datetime.datetime.strptime('Nov 20 2018', '%b %d %Y')
endDate = datetime.datetime.utcnow()
for streamer in get_streamers_with_the_most_viewers(4):
   x1, y1, s1, g1 = get_data(get_stream_data_for_user(streamer, startDate, endDate))

   plt.plot(s1, y1, label=str(streamer.display_name))
   length = s1.__len__()
plt.xlabel('from ' + datetime.datetime.strftime(startDate, "%b %d %Y") + ' time until ' + datetime.datetime.strftime(endDate, "%b %d %Y"))
plt.ylabel('viewers')
plt.title("Viewercounts")
plt.legend()
plt.show()"""
