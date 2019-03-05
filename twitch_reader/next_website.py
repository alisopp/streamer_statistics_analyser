import datetime

from model.db_initializer import DbConnector
from settings import env_variables
import statistics_reader
from website_generator import WebsiteGenerator

week_end_date = datetime.datetime.now().replace(minute=0, second=0, microsecond=0, hour=0) - datetime.timedelta(days=1)
week_end_date = week_end_date + datetime.timedelta(days=-((week_end_date.weekday() + 1) % 7))
week_end_date = week_end_date.replace(hour=23, minute=59)
DbConnector.getInstance().init_db(env_variables.db_url, env_variables.db_port, env_variables.db_name,
                                  env_variables.get_db_username(), env_variables.get_db_password())
generator = WebsiteGenerator(env_variables.wwwroot)
week_start_date = week_end_date - datetime.timedelta(weeks=1)
generator.generate_website(env_variables.debug, week_start_date, week_end_date,
                           [], statistics_reader.get_data_per_language, custom_title_pre="lang")
generator.generate_website(env_variables.debug, week_start_date, week_end_date,
                           ["Ninja", "ESL_CSGO", "OverwatchLeague"], statistics_reader.get_streamer_data,
                           custom_title_pre="streamer")
navigation_sides = [{"directory": "lang", "title": "Languages"}, {"directory": "streamer", "title": "Streamers"}]
start_date_of_the_website_generation = env_variables.start_date
start_date_of_the_website_generation = start_date_of_the_website_generation.replace(hour=23, minute=59)
generator.generate_navigation_side(start_date_of_the_website_generation, week_end_date, navigation_sides)
DbConnector.getInstance().close_db()
