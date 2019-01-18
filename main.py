# main entry file for the statistics
from model import db_initializer


def main():
    """
    main function
    """
    db_initializer.DbConnector.getInstance().close_db()


