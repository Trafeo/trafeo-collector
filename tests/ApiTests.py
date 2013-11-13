__author__ = 'Stephen Hoogendijk'
import os

# change the cwd to the main project directory
os.chdir(os.path.abspath('..'))

import Abstract.API as AbstractAPI
import unittest
import hashlib
import urllib2
import logging
import sys
from StringIO import StringIO

"""
This test covers the basic API implementation
"""


class CustomHTTPHandler(urllib2.HTTPHandler):
    def http_open(self, HTTTPrequest):
        logging.info("Custom HTTP Handler for API Test")
        return mock_response(HTTTPrequest)

class TestAPI(AbstractAPI.API):

    def basic_request(self):
        
        mock_opener = urllib2.build_opener(CustomHTTPHandler)
        urllib2.install_opener(mock_opener)

        uri = '%s/%s' % ('http://freegeoip.net/json', '127.0.0.1')
        #http_response = self.execute_request(uri)
        http_response = urllib2.urlopen(uri)

        return http_response.msg

class APItests(unittest.TestCase):

    control_hash = '4c6b55a94cf310c1277551dd231220fde2634cd3'
    test_api = {}

    def __init__(self, *args, **kwargs):
        super(APItests, self).__init__(*args, **kwargs)
        self.test_api = TestAPI()

    #FIXME: we don't need this test case!
    def testBasicRequest(self):
        """
        @return:
        """
        #NOTE: not sure if comparing hash is best for functional test aspect!
        test_hash = hashlib.sha1(self.test_api.basic_request())

        self.assertEqual(self.control_hash, test_hash.hexdigest())

def mock_response(HTTPrequest):
    if HTTPrequest.get_full_url() == "http://freegeoip.net/json/127.0.0.1":
        # INFO: http://epydoc.sourceforge.net/stdlib/urllib.addinfourl-class.html
        response = urllib2.addinfourl(StringIO("mock file"), "mock message", HTTPrequest.get_full_url())
        response.code = 200
        response.msg = '{"ip":"127.0.0.1","country_code":"RD","country_name":"Reserved","region_code":"","region_name":"","city":"","zipcode":"","latitude":0,"longitude":0,"metro_code":"","areacode":""}'
        return response
    else:
        # IDEA: May be its a good idea to run this into default handler
        print "unknown url, don't try to hack the test"
        sys.exit(0)

def main():
    unittest.main()

if __name__ == '__main__':
    main()

