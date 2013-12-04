__author__ = 'Stephen Hoogendijk'
import Collector.Traffic.API.Client as API
import time

class Collect:

    config = None
    api_client = None
    regions = {}
    db = None
    logger = None

    def __init__(self, config, api_client, db):
        """

        @param config:
        @type api_client: API.Client
        @param api_client:
        @param db:
        @return:
        """
        self.config = config
        self.api_client = api_client
        self.db = db
        self.logger = api_client.logger

        if not isinstance(api_client, API.Client):
            raise TypeError('Passed API client not a valid API client, type given: %s' % type(api_client))



    def add_region(self, name, region):
        """
        Add a region to process
        @param region:
        @return:
        """
        if type(region) is not dict or len(region) < 1:
           raise Exception('Invalid list of cities provided')

        self.regions[name] = region[name]
        return self

    def collect(self):

        result = {
            'success': 0,
            'failed': 0
        }

        if len(self.regions) > 0:

            for region_name in self.regions:
                region = self.regions[region_name]

                print '=> Collecting traffic data for: %s' % region_name.capitalize()
                self.logger.info('Collecting traffic data for %s' % region_name.capitalize())

                # get the data from the api and store it in mongo
                traffic_data = self.api_client.collect_traffic_by_region(region)

                if traffic_data is not None:
                    # save the traffic in mongodb
                    self.db.traffic.insert({
                        'ts': time.time(),
                        'data': traffic_data,
                        'region_info': region,
                        'region_name': region_name
                    })
                    result['success'] += 1

                else:
                    self.logger.error('Traffic collection failed for %s' % region_name)
                    result['failed'] += 1


        return result