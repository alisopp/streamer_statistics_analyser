from model import *
from model import Streamer

streamers = Streamer.objects.order_by('-highest_viewer_count').limit(10)

for streamer in streamers:
    print(streamer.user_name + ": " + str(streamer.highest_viewer_count))