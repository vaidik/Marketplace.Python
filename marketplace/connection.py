""" Provide connection with Marketplace API
"""

import json
import logging
import requests
import urllib

from requests.exceptions import HTTPError

log = logging.getLogger('marketplace.%s' % __name__)


class NotExpectedStatusCode(requests.exceptions.HTTPError):
    """ Raise if status code returned from API is not the expected one
    """
    pass


class Connection:
    """ Provides the way to connect to the Marketplace API.
    """

    CONNECTION_OBJ = None

    def __init__(self, auth_handler):
        self.auth = auth_handler

    @classmethod
    def get(cls, auth_handler=None):
        if cls.CONNECTION_OBJ is None:
            if auth_handler is not None:
                cls.CONNECTION_OBJ = Connection(auth_handler)
            else:
                raise Exception('Requires auth handler.')

        return cls.CONNECTION_OBJ

    @staticmethod
    def _get_error_reason(response):
        """Extract error reason from the response. It might be either
        the 'reason' or the entire response
        """
        try:
            body = response.json()
        except:
            raise Exception('API response is not valid JSON. %s'
                            % response.text)

        if body and 'reason' in body:
            return body['reason']
        return response.text

    def fetch(self, method, url, data=None, expected_status_code=None):
        """Prepare the headers, encode data, call API and provide
        data it returns
        """
        kwargs = self.auth.prepare_request(method, url, data)
        kwargs['headers']['Content-type'] = 'application/json'
        response = getattr(requests, method.lower())(url, **kwargs)
        log.debug(str(response.__dict__))
        if response.status_code >= 400:
            raise HTTPError('%s - %s' % (response.status_code, response.text))

        if (expected_status_code
                and response.status_code != expected_status_code):
            raise NotExpectedStatusCode(self._get_error_reason(response))
        return response

    def fetch_json(self, method, url, data=None, expected_status_code=None):
        """Return json decoded data from fetch
        """
        return self.fetch(method, url, data, expected_status_code).json()
