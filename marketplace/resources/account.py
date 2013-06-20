from urlparse import urlunparse

from marketplace.resources.apps import InstalledApp
from marketplace.resources.base import BaseResource
from marketplace.resources.permissions import Permissions
from marketplace.resources.settings import Settings


class Account(BaseResource):

    URIs = {
        'settings': 'account/settings/mine/',
        'permissions': 'account/permissions/mine/',
        'installed': 'account/installed/mine/',
        'feedback': 'account/feedback/',
        'newsletter': 'account/newsletter/',
    }

    @property
    def settings(self):
        if not hasattr(self, '_settings'):
            self.get_settings()

        return self._settings

    def get_settings(self):
        response = self.conn.fetch('GET', self.url('settings'))
        self._settings = self._convert_to_object(response, Settings)
        return self._settings

    @property
    def permissions(self):
        if not hasattr(self, '_permissions'):
            self.get_permissions()

        return self._permissions

    def get_permissions(self):
        response = self.conn.fetch('GET', self.url('permissions'))
        self._permissions = self._convert_to_object(response, Permissions)
        return self._permissions

    def submit_feedback(self, chromeless, feedback, platform, from_uri):
        data = dict(chromeless=chromeless, feedback=feedback,
                    platform=platform, from_uri=from_uri)
        self.conn.fetch('POST', self.url('feedback'), data)

    def subscribe_to_newsletter(self, email):
        self.conn.fetch('POST', self.url('newsletter'), dict(email=email))

    def get_installed_apps(self):
        response = self.conn.fetch('GET', self.url('installed'))
        return self._convert_to_object(response, InstalledApp)
