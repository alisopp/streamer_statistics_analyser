import time

import requests

from settings.credentials import client_id

"""
    Calls twitch for getting the streams list of a particular game. 
    Sorted by view count. Result are stored as a list in a JSON file.
"""


def read_twitch_streams():
    endpoint = "https://api.twitch.tv/helix/streams?user_login=dephilas"
    # endpoint = "https://api.twitch.tv/helix/games?id=0"
    # 31151431856
    # 31151446176
    # 31151617040
    all_data = []

    headers = {'Client-ID': client_id}
    result = requests.get(endpoint, headers=headers)
    json_data = result.json()
    # just add the data, leave aside the pagination cursor.
    all_data.extend(json_data["data"])

    return all_data


data = read_twitch_streams()
for entry in data:
    print entry
