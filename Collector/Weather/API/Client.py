__author__ = 'Stephen Hoogendijk'
import urllib
import urllib2
import logging

import Abstract.API as AbstractAPI


class Client(AbstractAPI.API):

    api_token = ''
    api_endpoint = ''
    data_format = 'json'
    logger = None

    def __init__(self, token, endpoint, logger):
        """

        @param token:
        @param endpoint:
        @type logger: logging
        @param logger:
        @return:
        """
        self.api_endpoint = endpoint
        self.api_token = token
        self.set_logger(logger)


    def get_weather_by_city(self, city):
        result = None

        try:
            api_uri = self.build_weather_api_url({
                'q' : city,
                'num_of_days' : 1,
                'key' : self.api_token
            })

            # make the request
            result = self.execute_request(api_uri)
        except Exception as exc:
            self.logger.error('Fetching weather data for %s failed, message: %s' % (city, exc.message))


        return result

    def build_weather_api_url(self, arguments):

        final_arguments = dict(arguments)
        final_arguments.update({
          'format' : self.data_format
        })

        return self.build_request_uri(self.api_endpoint, final_arguments)

