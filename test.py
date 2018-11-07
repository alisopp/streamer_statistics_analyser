from model import *
from model import Streamer

streamers = Streamer.objects.order_by('highes_viewer_count')

for streamer in streamers:
    print(streamer.user_name + ": " + str(streamer.highest_viewer_count))