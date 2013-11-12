__author__ = 'Stephen Hoogendijk'
import Collector.Weather.API.Client as API
import time

class Collect:

    config = {}
    api_client = {}
    cities = []
    db = {}

    def __init__(self, config, api_client, db):
        self.config = config
        self.api_client = api_client
        self.db = db

        if not isinstance(api_client, API.Client):
            raise TypeError('Passed API client not a valid API client, type given: %s' % type(api_client))



    def set_cities(self, cities):
        """
        Set the list of cities to process
        @param cities:
        @return:
        """
        if type(cities) is not list or len(cities) < 1:
           raise Exception('Invalid list of cities provided')

        self.cities = cities
        return self

    def collect(self):

        for city in self.cities:
            print '=> Collecting data for: %s' % city

            # get the data from the api and store it in mongo
            city_data =  self.api_client.get_weather_by_city(city)
            self.db.weather.insert({
                'ts' : time.time(),
                'data': city_data,
                'city': city
            })