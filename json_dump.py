import codecs
import json
import datetime
import read_streams

current_dt = datetime.datetime.utcnow()

with codecs.open("streams_"+str(current_dt).replace(" ", "_").replace(":","_")+".json", "w", "utf-8") as file:
    all_data = read_streams.readTwitchStreams()
    # closing file
    json.dump(all_data, file)
    file.close()