import json
import logging
import os
import unittest

from base64 import b64encode

import requests

from marketplace import resources
from marketplace.auth import OAuth
from marketplace.resources.base import BaseResource
from mock import Mock
from nose import SkipTest
from nose import tools
from nose.tools import eq_

import marketplace

log = logging.getLogger('test.%s' % __name__)

# Preparing to mock the requests
OLD_PATCH = requests.patch
OLD_POST = requests.post
OLD_PUT = requests.put
OLD_GET = requests.get
OLD_DELETE = requests.delete

MARKETPLACE_PORT = 443
MARKETPLACE_DOMAIN = 'marketplace-dev.allizom.org'
MARKETPLACE_PROTOCOL = 'https'


class Response:
    '''This is used to create a mock of response from API
    '''
    def __init__(self, status_code, content=''):
        self.status_code = status_code
        self.content = content
        self.text = content

    def json(self):
        return json.loads(self.text)


class MarketplaceTestCase(unittest.TestCase):

    class TestBaseResource(BaseResource):
        URIs = {
            'example': 'example/',
            'example_resource': 'example/%s/',
            'example_sub': 'example/%s/sub/%s/',
        }

    def setUp(self):
        self.auth = OAuth(consumer_key='consumer_key',
                          consumer_secret='consumer_secret')
        self.client = marketplace.Client(
            auth=self.auth,
            domain=MARKETPLACE_DOMAIN,
            port=MARKETPLACE_PORT,
            protocol=MARKETPLACE_PROTOCOL)

        self.sample_data = {
            'key1': 'value1',
            'key2': 'value2',
        }

    def tearDown(self):
        requests.patch = OLD_PATCH
        requests.post = OLD_POST
        requests.put = OLD_PUT
        requests.get = OLD_GET
        requests.delete = OLD_DELETE
