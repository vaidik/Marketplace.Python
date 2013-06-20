import json
import logging
import os
import unittest

from base64 import b64encode

import requests

from marketplace.auth import OAuth
from marketplace.tests.utils import MarketplaceTestCase
from marketplace.tests.utils import Response
from marketplace.tests.utils import (MARKETPLACE_PROTOCOL,
                                     MARKETPLACE_DOMAIN,
                                     MARKETPLACE_PORT)
from mock import Mock
from nose import SkipTest
from nose import tools
from nose.tools import eq_

import marketplace

log = logging.getLogger('test.%s' % __name__)


class TestClient(MarketplaceTestCase):

    def test_init(self):
        eq_(self.client.auth, self.auth)

        base_uri = '%s://%s:%s/api/v1/' % (MARKETPLACE_PROTOCOL,
                                           MARKETPLACE_DOMAIN,
                                           MARKETPLACE_PORT)
        eq_(self.client.base_uri, base_uri)

        from marketplace import connection
        self.assertIsInstance(self.client.conn, connection.Connection)

        from marketplace import resources
        self.assertIsInstance(self.client.account, resources.Account)
