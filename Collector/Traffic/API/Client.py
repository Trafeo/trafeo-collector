__author__ = 'Stephen Hoogendijk'
import urllib
import urllib2
import logging

import Abstract.API as AbstractAPI


class Client(AbstractAPI.API):

    config = None
    data_format = 'json'
    logger = None

    def __init__(self, config, logger):
        """

        @param config:
        @param logger:
        @return:
        """
        self.config = config
        self.set_logger(logger)


    def collect_traffic_by_region(self, region):
        """

        @param region:
        @return: collection traffic data for the given region
        """
        request = self.build_region_traffic_request(region)

        return self.execute_request(self.build_request_uri(request['uri'], request['data']))



    def build_region_traffic_request(self, region):
        """

        @param region:
        @return: returns a request object of uri and data
        """
        region_items = ['minY', 'minX', 'maxX', 'maxY', 'zoom']

        for item in region:
            if item not in region_items:
                raise Exception('Wrong region configuration item')


        if len(region) is not len(region_items):
            raise 'Missing configuration item, required region config : %s' % region

        base_url = self.config['api']['url']
        request_config = {
            'key': self.config['api']['key'],
            'projection': self.config['projection'],
            'language': self.config['language']
        }

        if base_url is None:
            raise Exception('Missing base url!')

        #check the configuration
        for config_chk in request_config:
            if config_chk is None or config_chk is '':
                raise Exception('Configuration item %s not set ' % config_chk)

        #build the request URI
        request_uri = "%s/s1/%2.2f,%2.2f,%2.2f,%2.2f/%d/%d/%s" % (base_url, region['minY'], region['minX'],
                                                                region['maxY'], region['maxX'], region['zoom'],
                                                                self.config['traffic_model_id'], 'json')

        return {
            'uri': request_uri,
            'data': request_config
        }