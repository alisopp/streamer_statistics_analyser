import datetime

from model.db_initializer import DbConnector
from settings import env_variables
import statistics_reader
from website_generator import WebsiteGenerator

outer_end_date = datetime.datetime.now()
outer_end_date = outer_end_date + datetime.timedelta(days=-((outer_end_date.weekday() + 1) % 7))
DbConnector.getInstance().init_db(env_variables.db_url, env_variables.db_port, env_variables.db_name,
                                  env_variables.get_db_username(), env_variables.get_db_password())
outer_end_date = outer_end_date.replace(hour=23, minute=59)
generator = WebsiteGenerator(env_variables.wwwroot)
outer_start_date = outer_end_date - datetime.timedelta(weeks=1)
generator.generate_website(env_variables.debug, outer_start_date, outer_end_date,
                           [], statistics_reader.get_data_per_language, custom_title_pre="lang")
generator.generate_navigation_side(env_variables.start_date, outer_end_date, ["lang", "streamer"])
DbConnector.getInstance().close_db()
