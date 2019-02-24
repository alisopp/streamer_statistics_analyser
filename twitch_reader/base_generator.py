import datetime

from model.db_initializer import DbConnector
from settings import env_variables
from website_generator import WebsiteGenerator
# minus one day to
outer_end_date = datetime.datetime.now().replace(minute=0, second=0, microsecond=0, hour=0) - datetime.timedelta(days=1)
outer_end_date = outer_end_date + datetime.timedelta(days=-((outer_end_date.weekday() + 1) % 7))
outer_end_date = outer_end_date.replace(hour=23, minute=59)
start_date = env_variables.start_date
start_date = start_date.replace(hour=23, minute=59)
DbConnector.getInstance().init_db(env_variables.db_url, env_variables.db_port, env_variables.db_name,
                                  env_variables.get_db_username(), env_variables.get_db_password())
generator = WebsiteGenerator(env_variables.wwwroot)

generator.generate_base_directory(env_variables.debug, start_date, outer_end_date, [])
DbConnector.getInstance().close_db()
