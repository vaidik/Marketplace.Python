from marketplace.resources.base import BaseResource
from urlparse import urlunparse


class Permissions(BaseResource):

    URIs = {
        'permissions': 'account/permissions/%s/',
    }
