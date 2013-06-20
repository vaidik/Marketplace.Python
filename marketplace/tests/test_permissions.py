import json
import logging
import os
import unittest

from base64 import b64encode

import requests

from marketplace import resources
from marketplace.auth import OAuth
from marketplace.tests.utils import MarketplaceTestCase
from marketplace.tests.utils import Response
from mock import Mock
from nose import SkipTest
from nose import tools
from nose.tools import eq_

import marketplace

log = logging.getLogger('test.%s' % __name__)


class TestPermissions(MarketplaceTestCase):

    def test_permissions_init(self):
        permissions_resp = {
            'permissions': {
                'admin': False,
                'developer': False,
                'localizer': False,
                'lookup': True,
                'reviewer': False
            },
            'resource_uri': '/api/v1/account/permissions/1/'
        }
        requests.get = Mock(return_value=Response(200,
                                                  json.dumps(
                                                      permissions_resp)))
        permissions = self.client.account.permissions

        self.assertIsInstance(permissions.URIs, dict)
