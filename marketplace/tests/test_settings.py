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


class TestSettings(MarketplaceTestCase):

    def test_settings_init(self):
        settings_resp = {
            'display_name': 'Test Display Name',
            'resource_uri': '/api/v1/account/settings/1/',
        }
        requests.get = Mock(return_value=Response(200,
                                                  json.dumps(settings_resp)))
        settings = self.client.account.settings

        self.assertIsInstance(settings.API_NAME, str)
        self.assertIsInstance(settings.ID_KEY, str)
        eq_(settings.ID_KEY, 'mine')
        self.assertIsInstance(settings.URIs, dict)
        self.assertIsInstance(settings.PATCHABLE_FIELDS, tuple)
        self.assertNotEquals(len(settings.PATCHABLE_FIELDS), 0)

    def test_settings_save(self):
        settings_resp = {
            'display_name': 'Test Display Name',
            'resource_uri': '/api/v1/account/settings/1/',
        }
        requests.get = Mock(return_value=Response(200,
                                                  json.dumps(settings_resp)))
        requests.patch = Mock(return_value=Response(202, ''))

        settings = self.client.account.settings
        display_name = settings.display_name

        settings.display_name = 'Test New Display Name'
        settings.save()
