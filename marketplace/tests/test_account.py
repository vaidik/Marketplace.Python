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


class TestAccount(MarketplaceTestCase):

    def test_submit_feedback(self):
        requests.post = Mock(return_value=Response(201))
        self.client.account.submit_feedback('Yes', 'A nice feedback.',
                                            'Desktop', '/home')

    def test_subscribe_to_newsletter(self):
        requests.post = Mock(return_value=Response(204))
        self.client.account.subscribe_to_newsletter('test@test.com')

    def test_get_installed_apps(self):
        installed_apps = {
            'meta': dict(),
            'objects': [dict() for i in range(3)],
        }
        requests.get = Mock(return_value=Response(200,
                                                  json.dumps(installed_apps)))
        apps = self.client.account.get_installed_apps()
        self.assertIsInstance(apps, list)
        for app in apps:
            self.assertIsInstance(app, resources.InstalledApp)

    def test_get_settings(self):
        settings_resp = {
            'display_name': 'Test Display Name',
            'resource_uri': '/api/v1/account/settings/1/',
        }
        requests.get = Mock(return_value=Response(200,
                                                  json.dumps(settings_resp)))
        self.assertIsInstance(self.client.account.settings, resources.Settings)
        self.assertIsInstance(self.client.account.get_settings(),
                              resources.Settings)
        self.assertIsInstance(self.client.account._settings,
                              resources.Settings)

    def test_settings_gets_cached_settings(self):
        settings_resp = {
            'display_name': 'Test Display Name',
            'resource_uri': '/api/v1/account/settings/1/',
        }
        requests.get = Mock(return_value=Response(200,
                                                  json.dumps(settings_resp)))
        settings = self.client.account.settings

        settings_resp['display_name'] = 'Updated Test Display Name'
        requests.get = Mock(return_value=Response(200,
                                                  json.dumps(settings_resp)))
        settings_old = self.client.account.settings
        settings_fresh = self.client.account.get_settings()

        # account.settings gets the cached value
        eq_(settings.display_name, settings_old.display_name)

        # account.get_settings() queries the server again
        self.assertNotEquals(settings_old.display_name,
                             settings_resp['display_name'])
        eq_(settings_fresh.display_name, settings_resp['display_name'])

        # account.get_settings() updates the cache
        eq_(settings_fresh.display_name,
            self.client.account.settings.display_name)

    def test_get_permissions(self):
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

        self.assertIsInstance(self.client.account.permissions,
                              resources.Permissions)
        self.assertIsInstance(self.client.account.get_permissions(),
                              resources.Permissions)
        self.assertIsInstance(self.client.account._permissions,
                              resources.Permissions)

    def test_permissions_gets_cached_permissions(self):
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

        permissions_resp['permissions']['admin'] = True
        requests.get = Mock(return_value=Response(200,
                                                  json.dumps(
                                                      permissions_resp)))
        permissions_old = self.client.account.permissions
        permissions_fresh = self.client.account.get_permissions()

        # account.permissions gets the cached value
        eq_(permissions.permissions['admin'],
            permissions_old.permissions['admin'])

        # account.get_permissions() queries the server again
        self.assertNotEquals(permissions_old.permissions['admin'],
                             permissions_resp['permissions']['admin'])
        eq_(permissions_fresh.permissions['admin'],
            permissions_resp['permissions']['admin'])

        # account.get_permissions() updates the cache
        eq_(permissions_fresh.permissions['admin'],
            self.client.account.permissions.permissions['admin'])
