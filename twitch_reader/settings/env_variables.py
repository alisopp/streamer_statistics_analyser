import datetime
import os

savePath = "D:/Miscellioneus/uni/BachelorArbeit/json_data"

runtimeDataFolder = "C:/Users/AIsop/PycharmProjects/twitch_streamer_statistics_reader/runtime_data/"

# in days
create_new_statistic_interval = 7


def get_debug():
    if os.environ.get('DEBUG') is not None:
        return os.environ['DEBUG'] == "True"
    return True

def get_db_username():
    if os.environ.get('DB_USERNAME') is not None:
        return os.environ['DB_USERNAME']
    return ''

def get_db_password():
    if os.environ.get('DB_PASSWORD') is not None:
        return os.environ['DB_PASSWORD']
    return ''

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
    return 27017


def get_start_date():
    if os.environ.get('START_DATE') is not None:
        result_date = datetime.datetime.strptime(os.environ['START_DATE'], "%d.%m.%Y")
    else:
        result_date = datetime.datetime.strptime("01.12.2018","%d.%m.%Y")
    return result_date + datetime.timedelta(days=(6 - result_date.weekday()))


# date from where all website should be generated
start_date = get_start_date()

db_url = get_url()

db_port = get_port()

db_name = "stream_reader"

db_password = get_db_password()
db_username = get_db_username()

wwwroot = get_www_root()

debug = get_debug()