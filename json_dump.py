import codecs
import json

from settings.env_variables import savePath


def json_save(all_data, current_dt):
    with codecs.open(savePath + "/streams_" + str(current_dt).replace(" ", "_").replace(":", "_") + ".json", "w",
                     "utf-8") as file:
        # closing file
        json.dump(all_data, file)
        file.close()
