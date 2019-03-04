import datetime
import os

import json_dump
import noise_data_generator
import statistics_reader
from template import navigation_generator, statistic_preview


class WebsiteGenerator:
    www_root = "/"

    def __init__(self, www_root):
        self.www_root = www_root

    def generate_base_directory(self, use_fake_data, start_date, end_date, languages, data_function, custom_title_pre=""):
        current = end_date
        while current > start_date:
            next_start_date = current + datetime.timedelta(days=-7)
            self.generate_website(use_fake_data, next_start_date, current, languages, data_function)
            current = next_start_date
        self.generate_navigation_side(start_date + datetime.timedelta(days=7), end_date)

    def generate_navigation_side(self, start_date, end_date):
        navigation_side = navigation_generator.generate_navigation(start_date, end_date)
        nav_file = open(self.www_root + "index.html", "w")
        nav_file.write(navigation_side)
        nav_file.close()

    def generate_website(self, use_fake_data, start_date, end_date, languages,data_function, custom_title_pre=""):
        website_data = {}
        if use_fake_data:
            website_data = noise_data_generator.generate_fake_data(5, start_date, end_date, languages)
        else:
            website_data = data_function(start_date, end_date, custom_title_pre, languages)

        directory = "side_" + end_date.strftime("%d.%m.%Y")
        index_side = statistic_preview.get_template(end_date.strftime("%d.%m.%Y"))

        if not os.path.exists(self.www_root + directory):
            os.makedirs(self.www_root + directory)
        file = open(self.www_root + directory + "/index.html", "w")
        file.write(index_side)
        file.close()
        json_dump.single_array_save(website_data, self.www_root + directory + "/data")
