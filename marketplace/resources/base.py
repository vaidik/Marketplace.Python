from urlparse import urljoin


class BaseResource(object):
    name = 'Base'
    URIs = {}

    def __init__(self, base_uri, conn):
        self.base_uri = base_uri
        self.conn = conn

        if not len(self.URIs.keys()):
            raise Exception('You have not defined URIs for your resource.')

    def url(self, key):
        """Builds URL for your API calls.
        """
        return urljoin(self.base_uri, self.URIs[key])
