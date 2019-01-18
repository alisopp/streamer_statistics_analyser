import os

savePath = "D:/Miscellioneus/uni/BachelorArbeit/json_data"

wwwroot = "C:/Users/AIsop/PycharmProjects/twitch_streamer_statistics_reader/example_website/"

runtimeDataFolder = "C:/Users/AIsop/PycharmProjects/twitch_streamer_statistics_reader/runtime_data/"

# in days
create_new_statistic_interval = 7


def get_url():
    if (os.environ.get('DB_HOST') is not None):
        return os.environ['DB_HOST']
    return '127.0.0.1'


def get_port():
    if (os.environ.get('DB_PORT') is not None):
        return int(os.environ['DB_PORT'])
    return 27017


db_url = get_url()

db_port = get_port()

db_name = "stream_reader"
