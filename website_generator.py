import datetime
import json
import os

import json_dump
import noise_data_generator
import statistics_reader
from model.db_initializer import DbConnector
from settings import env_variables


class WebsiteGenerator:
    www_root = "/"

    def __init__(self, www_root):
        self.www_root = www_root

    def generate_base_directory(self):
        print "not implemented"

    def generate_website(self, use_fake_data, start_date, end_date, languages):
        website_data = {}
        if use_fake_data:
            website_data = noise_data_generator.generate_fake_data(5, start_date, end_date, languages)
        else:
            website_data = statistics_reader.get_data_per_language(start_date, end_date, languages)
        os.remove(self.www_root + "side_1/data.json")
        os.rename(self.www_root + "side_2/data.json", self.www_root + "side_1/data.json")

        os.rename(self.www_root + "side_3/data.json", self.www_root + "side_2/data.json")
        os.rename(self.www_root + "side_4/data.json", self.www_root + "side_3/data.json")
        with open(self.www_root + 'index.json') as f:
            data = json.load(f)
            del data["date"][0]
            # "2018.11.05 - 2018.11.12"
            data["date"].append(start_date.strftime("%Y.%m.%d") + " - " + end_date.strftime("%Y.%m.%d"))
            json_dump.single_array_save(data, self.www_root + "index")
        json_dump.single_array_save(website_data, self.www_root + "side_4/data")


DbConnector.getInstance().init_db(env_variables.db_url, env_variables.db_port, env_variables.db_name)
generator = WebsiteGenerator(env_variables.wwwroot)
generator.generate_website(False, datetime.datetime.now() - datetime.timedelta(days=7),
                           datetime.datetime.now(),
                           [])
DbConnector.getInstance().close_db()
