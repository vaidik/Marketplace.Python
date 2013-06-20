import json
import logging
import unittest
import urllib

import requests
import oauth2 as oauth

from mock import Mock

from marketplace.auth import OAuth
from marketplace.connection import Connection
from marketplace.tests.utils import MarketplaceTestCase
from marketplace.tests.utils import Response

log = logging.getLogger('test.%s' % __name__)


class TestConnection(MarketplaceTestCase):

    def setUp(self):
        self.conn = Connection(OAuth(consumer_key='key',
                                     consumer_secret='secret'))

    def test_raising_on_httperror(self):
        resp = {"reason": "Error with OAuth headers"}
        requests.post = Mock(return_value=Response(401, json.dumps(resp)))
        self.assertRaises(requests.exceptions.HTTPError, self.conn.fetch,
                          'POST', 'http://example.com/', {})

        resp = "<html><title>404</title><body><p>Error 404</p></body></html>"
        requests.post = Mock(return_value=Response(404, resp))
        self.assertRaises(requests.exceptions.HTTPError, self.conn.fetch,
                          'POST', 'http://example.com/', {})

    def test_raising_on_unexpected(self):
        resp = {"reason": "Error with OAuth headers"}
        requests.post = Mock(return_value=Response(204, json.dumps(resp)))
        self.assertRaises(requests.exceptions.HTTPError, self.conn.fetch,
                          'POST', 'http://example.com/', {}, 201)

    def test_error_reason_json(self):
        resp = {"reason": "message"}
        self.assertEquals(
            Connection._get_error_reason(Response(204, json.dumps(resp))),
            resp['reason'])

    def test_error_reason_text(self):
        # when response body is JSON with reason as a top-level key
        resp = dict(reason='404. Page not found.')
        self.assertEquals(
            Connection._get_error_reason(Response(404, json.dumps(resp))),
            resp['reason'])

        # when response body is JSON without reason as a top-level key
        resp = json.dumps(dict(why='404. Page not found.'))
        self.assertEquals(
            Connection._get_error_reason(Response(404, resp)),
            resp)

        # when response body does not have JSON
        resp = '404 - Page does not exist.'
        self.assertRaises(Exception, Connection._get_error_reason,
                          Response(404, resp))

    def test_get(self):
        requests.get = Mock(return_value=Response(200, '{}'))
        self.conn.fetch('GET', 'http://ex.com')
        assert requests.get.called

    def test_post(self):
        requests.post = Mock(return_value=Response(201, '{}'))
        self.conn.fetch('POST', 'http://ex.com')
        assert requests.post.called

    def test_put(self):
        requests.put = Mock(return_value=Response(202, '{}'))
        self.conn.fetch('PUT', 'http://ex.com')
        assert requests.put.called

    def test_patch(self):
        requests.patch = Mock(return_value=Response(201, '{}'))
        self.conn.fetch('PATCH', 'http://ex.com')
        assert requests.patch.called

    def test_delete(self):
        requests.delete = Mock(return_value=Response(204, '{}'))
        self.conn.fetch('DELETE', 'http://ex.com')
        assert requests.delete.called
