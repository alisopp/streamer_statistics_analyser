import os

from jinja2 import Template, FileSystemLoader, Environment


def get_template(title):
    file_loader = FileSystemLoader(str(os.path.dirname(__file__)))
    env = Environment(loader=file_loader)

    template = env.get_template('statistics_preview.html')

    output = template.render(title=title)

    return output
