
""" Data collector module for trafeo """


try:
    import pymongo
    from pymongo import MongoClient
    import os
    import ConfigParser
    import logging
except ImportError as e:
    print 'Fatal: %s' % e.message
    exit(1)


# get a config file
def get_config(config_name):

    config_file = os.path.abspath('config'+'/'+config_name)

    if not os.path.exists(config_file):
        print "Config file '%s' does not exist!" % config_file
        exit(1)

    config = {}
    execfile(config_file, config)

    return config


class Collector:

    # local config file
    config = None
    db_client = None
    logger = None

    def __init__(self, config):
        """

        @param config:
        """
        self.config = config
        self.setup_db()
        self.set_logger()


    def setup_db(self):
        """

        @return:
        """
        db_name = self.config['db']['db_name']
        mongo_client = MongoClient('localhost', self.config['db']['db_port'])

        self.db_client = mongo_client[db_name]

    def set_logger(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)

        log_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'logs'))

        if not os.path.exists(log_path):
            print 'Logger directory %s not found' % log_path

        # create a file handler
        handler = logging.FileHandler(os.path.join(log_path, 'error.log'))
        handler.setLevel(logging.ERROR)

        # create a logging format
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        # add the handlers to the logger
        logger.addHandler(handler)

        self.logger = logger

    def get_logger(self):
        """
        Retrieve the logger instance
        @return:
        """
        return self.logger

    def get_db(self):
        """

        @return MongoClient:
        """
        return self.db_client
