import os

savePath = "D:/Miscellioneus/uni/BachelorArbeit/json_data"

runtimeDataFolder = "C:/Users/AIsop/PycharmProjects/twitch_streamer_statistics_reader/runtime_data/"

# in days
create_new_statistic_interval = 7


def get_www_root():
    if os.environ.get('WWW_ROOT') is not None:
        return os.environ['WWW_ROOT']
    return "C:/Users/AIsop/PycharmProjects/twitch_streamer_statistics_reader/example_website/"


def get_url():
    if os.environ.get('DB_HOST') is not None:
        return os.environ['DB_HOST']
    return '192.168.68.5'


def get_port():
    if os.environ.get('DB_PORT') is not None:
        return int(os.environ['DB_PORT'])
    return 27018


db_url = get_url()

db_port = get_port()

db_name = "stream_reader"

wwwroot = get_www_root()
