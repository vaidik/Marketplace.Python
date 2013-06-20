""" Provide connection with Marketplace API
"""

import json
import logging
import requests
import urllib

log = logging.getLogger('marketplace.%s' % __name__)


class NotExpectedStatusCode(requests.exceptions.HTTPError):
    """ Raise if status code returned from API is not the expected one
    """
    pass


class Connection:
    """ Provides the way to connect to the Marketplace API.
    """

    def __init__(self, auth_handler):
        self.auth = auth_handler

    @staticmethod
    def _get_error_reason(response):
        """Extract error reason from the response. It might be either
        the 'reason' or the entire response
        """
        body = response.json()
        if body and 'reason' in body:
            return body['reason']
        return response.content

    def fetch(self, method, url, data=None, expected_status_code=None):
        """Prepare the headers, encode data, call API and provide
        data it returns
        """
        kwargs = self.auth.prepare_request(method, url, data)
        kwargs['headers']['Content-type'] = 'application/json'
        response = getattr(requests, method.lower())(url, **kwargs)
        log.debug(str(response.__dict__))
        if response.status_code >= 400:
            response.raise_for_status()

        if (expected_status_code
                and response.status_code != expected_status_code):
            raise NotExpectedStatusCode(self._get_error_reason(response))
        return response

    def fetch_json(self, method, url, data=None, expected_status_code=None):
        """Return json decoded data from fetch
        """
        return self.fetch(method, url, data, expected_status_code).json()
