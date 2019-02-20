import datetime
import os

from jinja2 import FileSystemLoader, Environment


class Statistic:
    def __init__(self, link, link_name):
        self.link = link
        self.link_name = link_name

    link = ""
    link_name = ""


def generate_navigation(start_date, end_date):
    current = start_date
    statistics = []
    while current <= end_date:
        link_name = current.strftime("%d.%m.%Y")
        link = "side_" + link_name
        statistics.append(Statistic(link, link_name))
        current = current + datetime.timedelta(days=7)
    file_loader = FileSystemLoader(str(os.path.dirname(__file__)))
    env = Environment(loader=file_loader)
    template = env.get_template('navigation_preview.html')
    statistics.reverse()
    output = template.render(statistics=statistics)
    return output





