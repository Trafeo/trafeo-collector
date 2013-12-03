import Collector.Traffic.API.Client as API
import time

class Collect:

    config = None
    api_client = None
    cities = None
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

        if not isinstance(api_client, API.Client):
            raise TypeError('Passed API client not a valid API client, type given: %s' % type(api_client))

    def collect(self):

        result = {
            'success': 0,
            'failed': 0
        }

        for city in self.cities:
            print '=> Collecting data for: %s' % city

            # get the data from the api and store it in mongo
            city_data = self.api_client.get_weather_by_city(city)

            if city_data is not None:
                self.db.weather.insert({
                    'ts' : time.time(),
                    'data': city_data,
                    'city': city
                })
                result['success'] += 1

            else:
                result['failed'] += 1


        return result
