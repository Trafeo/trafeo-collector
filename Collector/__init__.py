
""" Data collector module for trafeo """


try:
    import pymongo
    import os
    import ConfigParser
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
