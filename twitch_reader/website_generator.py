import datetime
import os
import shutil

import json_dump
import noise_data_generator
import statistics_reader
from template import navigation_generator, statistic_preview
from template.navigation_generator import NavigationSideBuilder


class WebsiteGenerator:
    www_root = "/"

    def __init__(self, www_root):
        self.www_root = www_root

    def generate_base_directory(self, use_fake_data, start_date, end_date, filter_by, data_function,
                                custom_title_pre=""):
        shutil.rmtree(self.www_root + custom_title_pre, ignore_errors=True)
        current = end_date
        while current > start_date:
            next_start_date = current + datetime.timedelta(days=-7)
            self.generate_website(use_fake_data, next_start_date, current, filter_by, data_function, custom_title_pre)
            current = next_start_date

    def generate_navigation_side(self, start_date, end_date, sub_directories):
        nav_builder = NavigationSideBuilder()
        nav_builder = nav_builder.set_start_date(start_date).set_end_date(end_date)
        for sub_directory in sub_directories:
            nav_builder.add_sub_navigation(sub_directory["directory"],sub_directory["title"])

        navigation_side = nav_builder.build()
        nav_file = open(self.www_root + "index.html", "w")
        nav_file.write(navigation_side)
        nav_file.close()

    def generate_website(self, use_fake_data, start_date, end_date, filter_by, data_function, custom_title_pre):
        website_data = {}
        if use_fake_data:
            website_data = noise_data_generator.generate_fake_data(5, start_date, end_date, filter_by)
        else:
            website_data = data_function(start_date, end_date, custom_title_pre, filter_by)

        directory = "side_" + end_date.strftime("%d.%m.%Y")
        index_side = statistic_preview.get_template(end_date.strftime("%d.%m.%Y"))
        if not custom_title_pre.__eq__(""):
            custom_title_pre = "/" + custom_title_pre + "/"
        if not os.path.exists(self.www_root + custom_title_pre + directory):
            os.makedirs(self.www_root + custom_title_pre + directory)

        file = open(self.www_root + custom_title_pre + directory + "/index.html", "w")
        file.write(index_side)
        file.close()
        json_dump.single_array_save(website_data, self.www_root + custom_title_pre + directory + "/data")
