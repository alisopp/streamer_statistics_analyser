import os


def get_client_id():
    if os.environ.get('TWITCH_CREDENTIALS') is not None:
        return os.environ['TWITCH_CREDENTIALS']
    return ""


# secret client id to be set up with the twitch account
client_id = get_client_id()
