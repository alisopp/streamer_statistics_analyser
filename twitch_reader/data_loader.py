import datetime

import database_saver
import read_streams
from model.db_initializer import DbConnector
from settings import env_variables


class DataLoader:
    is_loading_data = True

    def __init__(self):
        pass

    def start(self):
        self.is_loading_data = True
        current_dt = datetime.datetime.utcnow()
        print("Start reading data")
        all_data = read_streams.read_twitch_streams(20)
        print("Saving data")
        database_saver.save_into_database(all_data, current_dt)
        # json_dump.json_save(all_data, current_dt)

    def shutdown(self):
        self.is_loading_data = False


DbConnector.getInstance().init_db(env_variables.db_url, env_variables.db_port, env_variables.db_name)
loader = DataLoader()
loader.start()
