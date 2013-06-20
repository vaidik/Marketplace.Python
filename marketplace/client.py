"""
A class to interact with Marketplace's API.

For full spec please read Marketplace API documentation

"""

import json
import logging
import mimetypes

from base64 import b64encode

import oauth2 as oauth

from urlparse import urlunparse

from . import resources
from .connection import Connection

log = logging.getLogger('marketplace.%s' % __name__)

MARKETPLACE_PORT = 443
MARKETPLACE_DOMAIN = 'marketplace.mozilla.org'
MARKETPLACE_PROTOCOL = 'https'


class Client:
    """A base class to authenticate and work with Marketplace API.
    """

    def __init__(self, auth, domain=MARKETPLACE_DOMAIN,
                 protocol=MARKETPLACE_PROTOCOL,
                 port=MARKETPLACE_PORT,
                 prefix=''):
        self.domain = domain
        self.protocol = protocol
        self.port = port
        self.prefix = prefix
        self.base_uri = urlunparse((self.protocol,
                                   '%s:%s' % (self.domain, self.port),
                                   '%s/api/v1' % self.prefix, '', '', ''))

        self.auth = auth
        self.conn = self.get_connection(auth)

        # all the resources get instantiated
        self.accounts = resources.Accounts(self.base_uri, self.conn)

    @staticmethod
    def get_connection(auth):
        """Provide Connection object used for communication with the API
        """
        return Connection(auth)
