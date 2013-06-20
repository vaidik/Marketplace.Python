from marketplace.resources.base import UpdateableResource


class Settings(UpdateableResource):
    API_NAME = 'settings'

    PATCHABLE_FIELDS = (
        'display_name',
    )

    URIs = {
        'settings': 'account/settings/%s/',
    }

    ID_KEY = 'mine'

    def save(self):
        for key in self._data.keys():
            self._data[key] = getattr(self, key)

        response = self.conn.fetch('PATCH', self.url(self.API_NAME,
                                                     (self.ID_KEY,)),
                                   self._patch_data)

        # Since Marketplace API only sometimes returns response body for
        # PATCH API requests
        if response.text != '':
            return self._convert_to_object(response, self.__class__)
