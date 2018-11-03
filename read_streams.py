
import time

import requests

from settings.credentials import client_id

"""
    Calls twitch for getting the streams list of a particular game. 
    Sorted by view count. Result are stored as a list in a JSON file.
"""


def read_twitch_streams():
    endpoint = "https://api.twitch.tv/helix/streams?first=100"

    all_data = []

    headers = {'Client-ID': client_id}
    result = requests.get(endpoint, headers=headers)
    json_data = result.json()
    # just add the data, leave aside the pagination cursor.
    all_data.extend(json_data["data"])

    cursor = (json_data["pagination"]["cursor"])  # cursor for the next page ...

    # fetch the next x pages ...
    for i in range(19):
        result = requests.get(endpoint + "&after=" + cursor, headers=headers)
        json_data = result.json()
        all_data.extend(json_data["data"])
        if "cursor" in json_data["pagination"]:
            cursor = (json_data["pagination"]["cursor"])  # cursor for the next page ...
        else:
            break
        time.sleep(3)  # should be 3 according to the Twitch regulations!
    return all_data
