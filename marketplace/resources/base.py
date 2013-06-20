import json

from marketplace.connection import Connection
from urlparse import urljoin


class APIObject(object):

    def __init__(self, data):
        self._data = data

        # set data keys as attributes to the object
        self.update_from(data)

    def update_from(self, data):
        for key, val in data.iteritems():
            self._data[key] = val
            setattr(self, key, val)

    @classmethod
    def create_from(cls, data):
        return cls(data)


class BaseResource(APIObject):
    name = 'Base'
    URIs = {}
    ID_KEY = None
    OBJECT_CLASS = None

    def __init__(self, base_uri, auth, data=None):
        if data is not None:
            APIObject.__init__(self, data)

        self.base_uri = base_uri
        self.auth = auth
        self.conn = Connection.get(auth)

        if not len(self.URIs.keys()):
            raise Exception('You have not defined URIs for your resource.')

    def url(self, key, format=None):
        """Builds URL for your API calls.
        """

        uri = (self.URIs[key] % format) if format else self.URIs[key]
        return urljoin(self.base_uri, uri)

    @classmethod
    def create_from(cls, data, obj):
        return cls(obj.base_uri, obj.auth, data)

    def _convert_to_object(self, data, cls):
        if hasattr(data, 'text'):
            _decoded = json.loads(data.text)
        else:
            _decoded = data

        if _decoded.get('objects', None):
            return [self._convert_to_object(obj, cls)
                    for obj in _decoded['objects']]
        else:
            return cls.create_from(_decoded, self)


class ListableResource(BaseResource):

    def __init__(self, base_uri, auth, data=None):
        if self.API_NAME is None:
            raise Exception('API_NAME property is not defined.')

        if self.OBJECT_CLASS is None:
            raise Exception('OBJECT_CLASS property is not defined.')

        BaseResource.__init__(self, base_uri, auth, data)

    def all(self):
        response = self.conn.fetch('GET', self.url(self.API_NAME))
        return self._convert_to_object(response, self.OBJECT_CLASS)


class CreateableResource(BaseResource):

    def __init__(self, base_uri, auth, data=None):
        if self.API_NAME is None:
            raise Exception('API_NAME property is not defined.')

        if self.OBJECT_CLASS is None:
            raise Exception('OBJECT_CLASS property is not defined.')

        BaseResource.__init__(self, base_uri, auth, data)

    def create(self, **kwargs):
        response = self.conn.fetch('POST', self.url(self.API_NAME), kwargs)
        return self._convert_to_object(response, self.OBJECT_CLASS)


class GetableResource(BaseResource):

    def __init__(self, base_uri, auth, data=None):
        if self.API_NAME is None:
            raise Exception('API_NAME property is not defined.')

        if self.OBJECT_CLASS is None:
            raise Exception('OBJECT_CLASS property is not defined.')

        BaseResource.__init__(self, base_uri, auth, data)

    def get(self, id):
        response = self.conn.fetch('GET', self.url(
            self.API_NAME) + ('%s/' % id))
        return self._convert_to_object(response, self.OBJECT_CLASS)


class DeleteableResource(BaseResource):

    def __init__(self, base_uri, auth, data=None):
        if self.API_NAME is None:
            raise Exception('API_NAME property is not defined.')

        if self.ID_KEY is None:
            raise Exception('ID_KEY property is not defined.')

        BaseResource.__init__(self, base_uri, auth, data)

    def delete(self):
        self.conn.fetch('DELETE', self.url(self.API_NAME, (self.ID_KEY,)))


class UpdateableResource(BaseResource):

    def __init__(self, base_uri, auth, data=None):
        if self.API_NAME is None:
            raise Exception('API_NAME property is not defined.')

        if self.ID_KEY is None:
            raise Exception('ID_KEY property is not defined.')

        BaseResource.__init__(self, base_uri, auth, data)

    @property
    def _patch_data(self):
        patch_data = {}

        try:
            for key in self.PATCHABLE_FIELDS:
                patch_data[key] = getattr(self, key)
        except AttributeError:
            # if PATCHABLE_FIELDS are not defined, then everything is PATCHABLE
            for key in self._data:
                patch_data[key] = getattr(self, key)

        return patch_data

    def save(self):
        for key in self._data.keys():
            self._data[key] = getattr(self, key)

        response = self.conn.fetch('PATCH', self.url(self.API_NAME,
                                                     (self.ID_KEY,)),
                                   self._patch_data)
