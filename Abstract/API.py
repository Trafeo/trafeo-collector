__author__ = 'Stephen Hoogendijk'

from abc import ABCMeta
import urllib
import urllib2
import time
import logging

class API:
    __metaclass__ = ABCMeta

    # limit one request per n seconds
    rate_limit = 0.5

    # a logger instance
    logger = None


    def execute_request(self, uri, data=None):
        """

        @param uri:
        @param data:
        @return:
        """

        time.sleep(self.rate_limit)
        try:

            if data is not None:
                encoded_data = urllib.urlencode(data)
            else:
                encoded_data = None

            request = urllib2.Request(uri, encoded_data)
            response = urllib2.urlopen(request)
            response_obj = response.read()

        except urllib2.HTTPError as http_error:
            raise Exception('API call failed: %s (http error)' % http_error)

        return response_obj

    def build_request_uri(self, url, arguments):
        """
        
        @param url:
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



    def set_logger(self, logger):
        """
        @type logger: logging
        @param logger: The logger to set in this API
        @return:
        """
        if not isinstance(logger, logging.getLoggerClass()):
            print 'You did not pass a valid instance of logging to this API client'
            exit(1)

        self.logger = logger

    def get_logger(self):
        """

        @return logging: Returns a logger instance
        """
        return self.logger