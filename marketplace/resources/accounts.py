from marketplace.resources import BaseResource
from urlparse import urlunparse


class Accounts(BaseResource):
    URIs = {
        'list': 'apps/app/',
        'settings': 'account/settings/mine/',
        'permissions': 'account/permissions/mine/',
        'newsletter': 'account/newsletter/',
        'installed_apps': 'account/installed/mine/',
        'feedback': 'account/feedback/',
    }

    def get_settings(self):
        """Get user settings.

        :returns: dict of user settings
        """

        response = self.conn.fetch('GET', self.url('settings'))
        return response

    def update_settings(self, display_name):
        """Update user settings.

        :returns: response
        """

        data = dict(display_name=display_name)
        response = self.conn.fetch('PATCH', self.url('settings'), data)
        return response

    def get_permissions(self):
        """Get user permissions.

        :returns: dict
        """

        response = self.conn.fetch('GET', self.url('permissions'))
        return response

    def get_installed_apps(self):
        """Get installed apps.

        :returns: dict
        """

        response = self.conn.fetch('GET', self.url('installed_apps'))
        return response

    def subscribe_newsletter(self, email):
        """Subscribe to newsletter.
        """

        data = dict(email=email)
        response = self.conn.fetch('POST', self.url('newsletter'), data=data)
        return response

    def submit_feedback(self, **kwargs):
        """Submit feedback to the Marketplace.
        """

        response = self.conn.fetch('POST', self.url('feedback'), data=kwargs)
        return response

    def list_installed_apps(self):
        """Lists all webapps owned by user

        :returns: list
        """

        response = self.conn.fetch('GET', self.url('list'))
        return response
