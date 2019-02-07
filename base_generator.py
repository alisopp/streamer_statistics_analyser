import datetime

from model.db_initializer import DbConnector
from settings import env_variables
from website_generator import WebsiteGenerator

outer_end_date = datetime.datetime.now().replace(minute=0, second=0, microsecond=0, hour=0)
outer_end_date = outer_end_date + datetime.timedelta(days=-((outer_end_date.weekday() + 1) % 7))
start_date = env_variables.start_date
DbConnector.getInstance().init_db(env_variables.db_url, env_variables.db_port, env_variables.db_name)
generator = WebsiteGenerator(env_variables.wwwroot)
generator.generate_base_directory(env_variables.debug, start_date, outer_end_date, [])
DbConnector.getInstance().close_db()
