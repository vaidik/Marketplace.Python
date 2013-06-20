import json
import logging
import os
import unittest

from base64 import b64encode

import requests

from marketplace.auth import OAuth
from marketplace.connection import Connection
from marketplace.resources.base import APIObject
from marketplace.resources.base import BaseResource
from marketplace.resources.base import CreateableResource
from marketplace.resources.base import DeleteableResource
from marketplace.resources.base import GetableResource
from marketplace.resources.base import ListableResource
from marketplace.resources.base import UpdateableResource
from marketplace.tests.utils import Response
from marketplace.tests.utils import MarketplaceTestCase
from mock import Mock
from nose import SkipTest
from nose import tools
from nose.tools import eq_

import marketplace

log = logging.getLogger('test.%s' % __name__)


class TestAPIObject(MarketplaceTestCase):

    def test_api_object_init(self):
        api_obj = APIObject(self.sample_data)
        self.assertIsInstance(api_obj._data, dict)
        self.assertDictEqual(api_obj._data, self.sample_data)

    def test_api_object_update_from_sets_attributes_on_object(self):
        more_sample_data = {
            'key3': 'value3',
            'key4': 'value4',
        }
        api_obj = APIObject(self.sample_data)
        api_obj.update_from(more_sample_data)
        self.assertDictContainsSubset(more_sample_data, api_obj._data)

        for key in more_sample_data.keys():
            eq_(getattr(api_obj, key), more_sample_data[key])

        for key in self.sample_data.keys():
            eq_(getattr(api_obj, key), self.sample_data[key])

    def test_create_from(self):
        api_obj = APIObject(self.sample_data)
        api_obj_new = api_obj.create_from(self.sample_data)
        self.assertIsInstance(api_obj_new, APIObject)


class TestBaseResource(MarketplaceTestCase):

    def test_base_resource_raises_exception_when_URI_is_not_set(self):
        class LocalTestResource(self.TestBaseResource):
            URIs = {}

        self.assertRaises(Exception, LocalTestResource, self.client.base_uri,
                          self.client.auth)

    def test_base_resource_init(self):
        resource = self.TestBaseResource(self.client.base_uri,
                                         self.client.auth)
        self.assertEquals(resource.base_uri, self.client.base_uri)
        self.assertEquals(resource.auth, self.client.auth)
        self.assertIsInstance(resource.conn, Connection)

        resource = self.TestBaseResource(self.client.base_uri,
                                         self.client.auth, self.sample_data)
        self.assertIsInstance(resource._data, dict)
        self.assertDictEqual(resource._data, self.sample_data)

        for key, val in self.sample_data.iteritems():
            self.assertEquals(getattr(resource, key), val)

    def test_url_construction(self):
        resource = self.TestBaseResource(self.client.base_uri,
                                         self.client.auth)

        self.assertEquals(resource.url('example'),
                          '%s%s' % (self.client.base_uri,
                                    resource.URIs['example']))

        self.assertEquals(resource.url('example_sub', (1, 2)),
                          '%s%s' % (self.client.base_uri,
                                    (resource.URIs['example_sub'] % (1, 2))))

    def test_create_from(self):
        resource = self.TestBaseResource(self.client.base_uri,
                                         self.client.auth)
        resource_new = self.TestBaseResource.create_from(self.sample_data,
                                                         resource)
        self.assertIsInstance(resource, BaseResource)

    def test_convert_singlur_resource_to_object(self):
        response = Response(200, json.dumps(self.sample_data))
        resource = self.TestBaseResource(self.client.base_uri,
                                         self.client.auth)
        new_resource = resource._convert_to_object(response,
                                                   self.TestBaseResource)
        self.assertIsInstance(new_resource, self.TestBaseResource)

    def test_convert_plural_resource_to_object(self):
        response_body = json.dumps({
            'objects': [self.sample_data for i in range(5)]
        })
        response = Response(200, response_body)
        resource = self.TestBaseResource(self.client.base_uri,
                                         self.client.auth)
        new_resources = resource._convert_to_object(response,
                                                    self.TestBaseResource)
        self.assertIsInstance(new_resources, list)
        for i in range(5):
            self.assertIsInstance(new_resources[i], self.TestBaseResource)


class TestListableResource(MarketplaceTestCase):

    def setUp(self):
        MarketplaceTestCase.setUp(self)

        class TestListableResource(self.TestBaseResource, ListableResource):
            API_NAME = 'example'
            OBJECT_CLASS = None
        TestListableResource.OBJECT_CLASS = TestListableResource

        self.TestListableResource = TestListableResource

    def test_listable_resource_raises_exception(self):
        # when only API_NAME is set
        class LocalTestResource(self.TestListableResource):
            API_NAME = 'api_name'
            OBJECT_CLASS = None

        self.assertRaises(Exception, LocalTestResource, self.client.base_uri,
                          self.client.auth)

        # when only OBJECT_CLASS is set
        class LocalTestResource(TestBaseResource, ListableResource):
            API_NAME = None
            OBJECT_CLASS = 'SomeClass'

        self.assertRaises(Exception, LocalTestResource, self.client.base_uri,
                          self.client.auth)

    def test_all_method(self):
        requests.get = Mock(return_value=Response(200, json.dumps({
            'objects': [self.sample_data for i in range(5)],
        })))
        #tools.set_trace()
        resource = self.TestListableResource(self.client.base_uri,
                                             self.client.auth)
        objects = resource.all()
        self.assertIsInstance(objects, list)
        for obj in objects:
            self.assertIsInstance(obj, self.TestListableResource)


class TestCreatableResource(MarketplaceTestCase):

    def setUp(self):
        MarketplaceTestCase.setUp(self)

        class TestResource(self.TestBaseResource, CreateableResource):
            API_NAME = 'example'
            OBJECT_CLASS = None
        TestResource.OBJECT_CLASS = TestResource

        self.TestResource = TestResource

    def test_createable_resource_raises_exception(self):
        # when only API_NAME is set
        class LocalTestResource(self.TestBaseResource, CreateableResource):
            API_NAME = 'api_name'

        self.assertRaises(Exception, LocalTestResource, self.client.base_uri,
                          self.client.auth)

        # when only OBJECT_CLASS is set
        class LocalTestResource(self.TestBaseResource, CreateableResource):
            OBJECT_CLASS = 'SomeClass'

        self.assertRaises(Exception, LocalTestResource, self.client.base_uri,
                          self.client.auth)

    def test_create_method(self):
        mock_response = Response(201, json.dumps(self.sample_data))
        requests.post = Mock(return_value=mock_response)
        resource = self.TestResource(self.client.base_uri, self.client.auth)
        objects = resource.create(**self.sample_data)
        self.assertIsInstance(objects, self.TestResource)


class TestGetableResource(MarketplaceTestCase):

    def setUp(self):
        MarketplaceTestCase.setUp(self)

        class TestResource(self.TestBaseResource, GetableResource):
            API_NAME = 'example_resource'
            OBJECT_CLASS = None
        TestResource.OBJECT_CLASS = TestResource

        self.TestResource = TestResource

    def test_getable_resource_raises_exception(self):
        # when only API_NAME is set
        class LocalTestResource(GetableResource):
            API_NAME = 'api_name'

        self.assertRaises(Exception, LocalTestResource, self.client.base_uri,
                          self.client.auth)

        # when only OBJECT_CLASS is set
        class LocalTestResource(GetableResource):
            OBJECT_CLASS = 'SomeClass'

        self.assertRaises(Exception, LocalTestResource, self.client.base_uri,
                          self.client.auth)

    def test_get_method(self):
        mock_response = Response(200, json.dumps(self.sample_data))
        requests.get = Mock(return_value=mock_response)
        resource = self.TestResource(self.client.base_uri, self.client.auth)
        objects = resource.get(id='some_id')
        self.assertIsInstance(objects, self.TestResource)


class TestDeleteaableResource(MarketplaceTestCase):

    def setUp(self):
        MarketplaceTestCase.setUp(self)

        class TestResource(self.TestBaseResource, DeleteableResource):
            API_NAME = 'example_resource'
            ID_KEY = 'key1'

        self.TestResource = TestResource

    def test_deleteable_resource_raises_exception(self):
        # when only API_NAME is set
        class LocalTestResource(self.TestBaseResource, DeleteableResource):
            API_NAME = 'api_name'

        self.assertRaises(Exception, LocalTestResource, self.client.base_uri,
                          self.client.auth)

        # when only ID_KEY is set
        class LocalTestResource(self.TestBaseResource, DeleteableResource):
            ID_KEY = 'some_key'

        self.assertRaises(Exception, LocalTestResource, self.client.base_uri,
                          self.client.auth)

    def test_delete_method(self):
        requests.delete = Mock(return_value=Response(204))
        resource = self.TestResource(self.client.base_uri, self.client.auth,
                                     self.sample_data)
        resource.delete()


class TestUpdateaableResource(MarketplaceTestCase):

    def setUp(self):
        MarketplaceTestCase.setUp(self)

        class TestResource(self.TestBaseResource, UpdateableResource):
            API_NAME = 'example_resource'
            ID_KEY = 'key1'

        self.TestResource = TestResource

    def test_updateable_resource_raises_exception(self):
        # when only API_NAME is set
        class LocalTestResource(self.TestBaseResource, UpdateableResource):
            API_NAME = 'api_name'

        self.assertRaises(Exception, LocalTestResource, self.client.base_uri,
                          self.client.auth)

        # when only ID_KEY is set
        class LocalTestResource(self.TestBaseResource, UpdateableResource):
            ID_KEY = 'some_key'

        self.assertRaises(Exception, LocalTestResource, self.client.base_uri,
                          self.client.auth)

    def test_save_method(self):
        requests.patch = Mock(return_value=Response(200))
        resource = self.TestResource(self.client.base_uri, self.client.auth,
                                     self.sample_data)
        resource.key1 = 'new_value1'
        resource.save()

        self.assertEquals(resource._data['key1'], resource.key1)

    def test_patch_data(self):
        class LocalTestResource(self.TestBaseResource, UpdateableResource):
            API_NAME = 'example'
            ID_KEY = 'key1'
            PATCHABLE_FIELDS = ('key2',)

        patch_data = {
            'key2': 'new_value2',
        }

        resource = LocalTestResource(self.client.base_uri, self.client.auth,
                                     self.sample_data)
        resource.key2 = 'new_value2'
        self.assertIsInstance(resource._patch_data, dict)
        self.assertDictEqual(resource._patch_data, patch_data)
        self.assertEquals(resource._patch_data['key2'], resource.key2)
