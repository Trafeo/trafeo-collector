__author__ = 'Stephen Hoogendijk'

from abc import ABCMeta
import urllib
import urllib2
import time

class API:
    __metaclass__ = ABCMeta

    # limit one request per n seconds
    rate_limit = 0.5

    def execute_request(self, uri, data=None):
        """

        @param uri:
        @param data:
        @return:
        """
        response_obj = None

        time.sleep(self.rate_limit)
        try:
            response = urllib2.urlopen(uri, data)
            response_obj = response.read()

        except urllib2.HTTPError as http_error:
            print 'API call failed: %s (http error)' % http_error

        return response_obj

    def build_request_uri(self, url, arguments):
        """

        @param arguments:
        @return:
        """
        if len(arguments) == 0:
            raise Exception('Arguments passed to build_request_uri are invalid')

        if url.find('?') is not -1:
            raise Exception('URL %s is not valid, endpoint should not contain a question mark (?)' % url)


        arg_string =  urllib.urlencode(arguments)

        return url + '?' + arg_string


    def set_rate_limit(self, seconds):
        """

        @param seconds integer:
        @return:
        """
        self.rate_limit = int(seconds)

    def set_data_format(self, data_format):
        """

        @param data_format:
        @return:
        """

        if data_format not in ['json', 'xml']:
            raise Exception('Invalid data format: %s, only json and xml are valid data types for this api stack' % data_format)

        self.data_format = data_format