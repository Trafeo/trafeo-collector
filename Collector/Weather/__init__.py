__author__ = 'Stephen Hoogendijk'

from pymongo import MongoClient

class Weather:

    # local config file
    config = {}
    db_client = {}

    def __init__(self, config):
        """

        @param config:
        """
        self.config = config
        self.setup_db()


    def setup_db(self):
        """

        @return:
        """
        db_name = self.config['db']['db_name']
        mongo_client = MongoClient('localhost', self.config['db']['db_port'])

        self.db_client = mongo_client[db_name]

    def get_db(self):
        """

        @return MongoClient:
        """
        return self.db_client
