__author__ = 'Stephen Hoogendijk'
import urllib
import urllib2

import Abstract.API as AbstractAPI


class Client(AbstractAPI.API):

    api_token = ''
    api_endpoint = ''
    data_format = 'json'

    def __init__(self, token, endpoint):
        """

        @param token: Api token for collecting weather data
        @param cities: List of cities to collect weather from

        """
        self.api_endpoint = endpoint
        self.api_token = token

    def get_weather_by_city(self, city):

        api_uri = self.build_weather_api_url({
            'q' : city,
            'num_of_days' : 5,
            'key' : self.api_token
        })

        # make the request
        return self.execute_request(api_uri)

    def build_weather_api_url(self, arguments):

        final_arguments = dict(arguments)
        final_arguments.update({
          'format' : self.data_format
        })

        return self.build_request_uri(self.api_endpoint, final_arguments)