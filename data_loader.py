import datetime
import time

import database_saver
import json_dump
import read_streams

while True:
    current_dt = datetime.datetime.utcnow()
    print("Start reading data")
    all_data = read_streams.read_twitch_streams(20)
    print("Saving data")
    database_saver.save_into_database(all_data, current_dt)
    json_dump.json_save(all_data, current_dt)
    print("Wait 5 minutes")
    time.sleep(300)
