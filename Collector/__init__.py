
""" Data collector module for trafeo """


try:
    import pymongo
    from pymongo import MongoClient
    import os
    import ConfigParser
    import logging
    from shutil import copyfile
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

        # if the log rotator does not exist, create it
        if not os.path.exists('/etc/logrotate.d/collect'):
            copyfile(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config', 'logrotate-collect')),
                     '/etc/logrotate.d/collect')

        # create the directory for logging
        if not os.path.exists('/var/log/collect'):
            os.mkdir('/var/log/collect')

        self.set_logger()


    def setup_db(self):
        """

        @return:
        """
        db_name = self.config['db']['db_name']
        mongo_client = MongoClient('localhost', self.config['db']['db_port'])


        self.db_client = mongo_client[db_name]

        if self.config['db']['db_user'] is not '':
            self.db_client.authenticate(self.config['db']['db_user'], self.config['db']['db_pass'])

    def set_logger(self):
        """
        Set the logger instance (void)
        @return:
        """
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)

        # try to get the logger directory from the config, if it does not exist, fall back to the default
        log_path = '/var/log/collect'

        if not os.path.exists(log_path):
            os.mkdir(log_path)

        # create a file handler
        error_handler = logging.FileHandler(os.path.join(log_path, 'error.log'))
        error_handler.setLevel(logging.ERROR)

        info_handler = logging.FileHandler(os.path.join(log_path, 'information.log'))
        info_handler.setLevel(logging.INFO)

        # create a logging format
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        error_handler.setFormatter(formatter)
        info_handler.setFormatter(formatter)

        # add the handlers to the logger
        logger.addHandler(error_handler)
        logger.addHandler(info_handler)

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
