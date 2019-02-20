from mongoengine import *

from settings import env_variables


class DbConnector:
    __instance = None

    db_client = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if DbConnector.__instance == None:
            DbConnector()
        return DbConnector.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if DbConnector.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            DbConnector.__instance = self

    def init_db(self, db_url, db_port, db_name, username, password):
        if self.db_client == None:
            self.db_client = connect(db_name, username=username, password=password, authentication_source='admin', host=db_url, port=db_port)

    def close_db(self):
        if self.db_client != None:
            self.db_client.close()
        self.db_client = None
