import datetime

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
            #td = parser.parse(str(entry.observation_date)) - datetime.datetime(1970, 1, 1)
            cnt = cnt + 1
            x.append(cnt)
            y.append(entry.viewer_count)
            s.append(dates.datestr2num(date_tmp))
            # s.append(td)
    return (x, y, s, game_id)


startDate = datetime.datetime.strptime('Nov 20 2018', '%b %d %Y')
endDate = datetime.datetime.utcnow()
streamer = get_streamers_with_the_most_viewers(1).first()
x1, y1, s1, g1 = get_data(get_stream_data_for_user(get_streamers_with_the_most_viewers(1).first(), startDate, endDate))

plt.plot(s1, y1, label=str(streamer.display_name))
length = s1.__len__()
plt.axis([s1[0], s1[length - 1], 0, streamer.highest_viewer_count])
plt.xlabel('from ' + datetime.datetime.strftime(startDate, "%b %d %Y") + ' time until ' + datetime.datetime.strftime(endDate, "%b %d %Y"))
plt.ylabel('viewers')
plt.title(str(streamer.display_name) + "`s viewercounts")
plt.legend()
plt.show()
plt.show()
