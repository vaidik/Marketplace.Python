import json
import logging
import unittest
import urllib

import requests
import oauth2 as oauth

from mock import Mock

from marketplace.auth import AuthHandler, OAuth
from marketplace.connection import Connection
from marketplace.tests.utils import MarketplaceTestCase
from marketplace.tests.utils import Response

log = logging.getLogger('test.%s' % __name__)


class TestAuth(MarketplaceTestCase):

    def test_auth_handler_raises_exception_for_prepare_request(self):
        auth = AuthHandler()
        self.assertRaises(NotImplementedError, auth.prepare_request)

    def test_oauth_init(self):
        oauth_handler = OAuth('key', 'secret')
        self.assertIsInstance(oauth_handler.consumer, oauth.Consumer)

    def test_oauth_get_oauth_args(self):
        oauth_key = 'key'
        oauth_secret = 'secret'

        oauth_handler = OAuth(oauth_key, oauth_secret)
        oauth_args = oauth_handler._get_oauth_args()

        self.assertEquals(oauth_args['oauth_version'], '1.0')
        self.assertIsInstance(oauth_args['oauth_timestamp'], int)
        self.assertIsInstance(oauth_args['oauth_nonce'], str)
        self.assertEquals(oauth_args['oauth_signature_method'], 'HMAC-SHA1')
        self.assertEquals(oauth_args['oauth_consumer_key'], oauth_key)

    def test_oauth_prepare_request(self):
        oauth_handler = OAuth('key', 'secret')
        data = {"some": "data"}

        prepared = oauth_handler.prepare_request('GET', 'http://example.com')
        self.assertIsInstance(prepared, dict)
        self.assertIsInstance(prepared['headers'], dict)
        self.assertEquals(prepared['data'], '')
        self.assertIsInstance(prepared['headers']['Authorization'], unicode)
        self.assertNotEquals(len(prepared['headers']['Authorization']), 0)

        prepared = oauth_handler.prepare_request('GET', 'http://example.com',
                                                 data)
        self.assertIsInstance(prepared, dict)
        self.assertIsInstance(prepared['headers'], dict)
        self.assertEquals(prepared['data'], urllib.urlencode(data))

        prepared = oauth_handler.prepare_request('POST', 'http://example.com',
                                                 data)
        self.assertIsInstance(prepared, dict)
        self.assertIsInstance(prepared['headers'], dict)
        self.assertEquals(prepared['data'], json.dumps(data))
