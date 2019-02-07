import datetime

from model.db_initializer import DbConnector
from settings import env_variables
from website_generator import WebsiteGenerator

outer_end_date = datetime.datetime.now() + datetime.timedelta(weeks=2)
outer_end_date = outer_end_date + datetime.timedelta(days=-((outer_end_date.weekday() + 1) % 7))
DbConnector.getInstance().init_db(env_variables.db_url, env_variables.db_port, env_variables.db_name)
generator = WebsiteGenerator(env_variables.wwwroot)
generator.generate_website(env_variables.debug, outer_end_date - datetime.timedelta(weeks=1), outer_end_date,
                           [])
generator.generate_navigation_side(env_variables.start_date, outer_end_date)
DbConnector.getInstance().close_db()
