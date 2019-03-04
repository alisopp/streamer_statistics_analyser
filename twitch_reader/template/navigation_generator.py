import datetime
import os

from jinja2 import FileSystemLoader, Environment


class Statistic:
    def __init__(self, link, link_name):
        self.link = link
        self.link_name = link_name

    link = ""
    link_name = ""


class SubDirectory:
    def __init__(self, directory, title):
        self.directory = directory
        self.title = title

    directory = ""
    title = ""


class NavigationSideBuilder:
    sub_directories = []
    start_date = datetime
    end_date = datetime

    def __init__(self):
        pass

    def add_sub_navigation(self, sub_directory, sub_title):
        self.sub_directories.append(SubDirectory(sub_directory,sub_title))
        return self

    def set_start_date(self, start_date):
        self.start_date = start_date
        return self

    def set_end_date(self, end_date):
        self.end_date = end_date
        return self

    def build(self):
        current = self.start_date
        statistics = []
        while current <= self.end_date:
            next_end_date = current + datetime.timedelta(days=7)
            link_name = current.strftime("%d.%m.%Y")
            link = "side_" + link_name
            link_name += " - " + next_end_date.strftime("%d.%m.%Y")
            statistics.append(Statistic(link, link_name))
            current = next_end_date
        file_loader = FileSystemLoader(str(os.path.dirname(__file__)))
        env = Environment(loader=file_loader)
        template = env.get_template('navigation_preview.html')
        statistics.reverse()
        output = template.render(statistics=statistics, sub_directories=self.sub_directories)
        return output
