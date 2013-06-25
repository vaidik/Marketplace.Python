from marketplace.resources import BaseResource
from urlparse import urlunparse


class Payments(BaseResource):
    URIs = {
        'tiers': 'webpay/prices/',
        'tier': 'webpay/prices/%s/'
    }

    def get_tiers(self):
        """Lists all payment tiers

        :returns: list
        """

        response = self.conn.fetch('GET', self.url('tiers'))
        return response

    def get_tier(self, id):
        """Get a payment tier

        :returns: list
        """

        response = self.conn.fetch('GET', self.url('tier', (id,)))
        return response
