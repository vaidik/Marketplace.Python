from marketplace.resources import BaseResource
from urlparse import urlunparse


class Accounts(BaseResource):
    URIs = {
        'list': 'apps/app/',
    }

    def list_webapps(self):
        """Lists all webapps owned by user

        :returns: list
        """

        response = self.conn.fetch('GET', self.url('list'))
        return response
