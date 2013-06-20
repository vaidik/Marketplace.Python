import json
import oauth2 as oauth
import time
import urllib


class AuthHandler(object):
    """Basic AuthHandler to prepare different types of authenticated requests.
    """

    def prepare_request(self):
        """Prepares headers and body depending upon the type of request.
        Must be implemented by the class extending this class.
        """
        raise NotImplementedError


class OAuth(AuthHandler):

    signature_method = oauth.SignatureMethod_HMAC_SHA1()

    def __init__(self, consumer_key, consumer_secret):
        self.set_consumer(consumer_key, consumer_secret)

    def set_consumer(self, consumer_key, consumer_secret):
        """Sets the consumer attribute
        """
        self.consumer = oauth.Consumer(consumer_key, consumer_secret)

    def _get_oauth_args(self):
        """Provide a dict with oauth data
        """
        return dict(
            oauth_consumer_key=self.consumer.key,
            oauth_nonce=oauth.generate_nonce(),
            oauth_signature_method='HMAC-SHA1',
            oauth_timestamp=int(time.time()),
            oauth_version='1.0')

    def prepare_request(self, method, url, body=''):
        """Prepares headers and body for sending OAuth signed requests.

        :returns: headers of the signed request
        """
        req = oauth.Request(method=method, url=url,
                            parameters=self._get_oauth_args())
        req.sign_request(self.signature_method, self.consumer, None)

        headers = req.to_header()

        if body:
            if method == 'GET':
                body = urllib.urlencode(body)
            else:
                body = json.dumps(body)

        return {"headers": headers, "data": body}
