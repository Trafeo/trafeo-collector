__author__ = 'Stephen Hoogendijk'
import os

# change the cwd to the main project directory
os.chdir(os.path.abspath('..'))

import Abstract.API as AbstractAPI
import unittest
import hashlib

"""
This test covers the basic API implementation
"""

class TestAPI(AbstractAPI.API):

    def basic_request(self):
        uri = '%s/%s' % ('http://freegeoip.net/json', '127.0.0.1')

        return self.execute_request(uri)

class APItests(unittest.TestCase):

    control_hash = '4c6b55a94cf310c1277551dd231220fde2634cd3'
    test_api = {}

    def __init__(self, *args, **kwargs):
        super(APItests, self).__init__(*args, **kwargs)
        self.test_api = TestAPI()

    def testBasicRequest(self):
        """

        @return:
        """
        test_hash = hashlib.sha1(self.test_api.basic_request())

        self.assertEqual(self.control_hash, test_hash.hexdigest())



def main():
    unittest.main()

if __name__ == '__main__':
    main()
