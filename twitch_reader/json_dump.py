import codecs
import datetime
import json
from bson import json_util

from settings.env_variables import savePath


def json_save(all_data, current_dt):
    with codecs.open(savePath + "/streams_" + str(current_dt).replace(" ", "_").replace(":", "_") + ".json", "w",
                     "utf-8") as file:
        # closing file
        json.dump(all_data, file)
        file.close()


def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()


def single_array_save(data, filename):
    with codecs.open(filename + ".json", "w",
                     "utf-8") as file:
        # closing file
        #data = json.dumps(data, )
        json.dump(data, file,default = myconverter)
        file.close()
