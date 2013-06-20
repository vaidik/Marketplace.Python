from marketplace.resources.base import BaseResource
from marketplace.resources.base import CreateableResource
from marketplace.resources.base import DeleteableResource
from marketplace.resources.base import GetableResource
from marketplace.resources.base import ListableResource
from marketplace.resources.base import UpdateableResource
from urlparse import urlunparse


class BaseApp(BaseResource):
    API_NAME = 'app'

    URIs = {
        'app': 'apps/app/%s/',
    }

    def __repr__(self):
        return '<%(module)s.%(class)s object (App Name: %(app_name)s)>' % {
            'module': __name__,
            'class': self.__class__.__name__,
            'app_name': self._data['name'],
        }


class App(BaseApp, DeleteableResource, UpdateableResource):
    pass


class InstalledApp(BaseApp):
    URIs = {
        'app': 'apps/app/%s/',
        'installed': 'account/installed/mine/'
    }


class Apps(CreateableResource, GetableResource, ListableResource):
    API_NAME = 'app'

    OBJECT_CLASS = App

    URIs = {
        'app': 'apps/app/',
    }
