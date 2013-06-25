from marketplace.resources import BaseResource
from urlparse import urlunparse


class Apps(BaseResource):
    URIs = {
        'app': 'apps/app/%s/',
        'app_privacy': 'apps/app/%s/privacy/',
        'apps': 'apps/app/',
        'validate': 'apps/validation/',
        'categories': 'apps/category/',
        'screenshot': 'apps/preview/',
        'status': 'apps/status/%s/',
    }

    def validate_app(self, manifest=None, packaged=None):
        """Validates an app for submission.

        :returns: dict
        """

        if manifest and packaged:
            raise Exception('''Either provide manifest for hosted app or '''
                            '''details of packaged app.''')

        if manifest:
            data = dict(manifest=manifest)

        if packaged:
            valid = (packaged.get('type') and packaged.get('data') and
                     packaged.get('name'))
            if valid:
                data = dict(upload=packaged)
            else:
                raise Exception('Incomplete data provided for packaged app.')

        response = self.conn.fetch('POST', self.url('validate'), data)
        return response

    def get_validation(self, id):
        """Get an existing validation.

        :returns: dict
        """

        response = self.conn.fetch('GET', self.url('validation', (id,)))
        return response

    def get_apps(self):
        """Get a list of developed apps.
        """

        response = self.conn.fetch('GET', self.url('apps'))
        return response

    def get_app(self, slug=None, id=None):
        """Get an app.
        """

        response = self.conn.fetch('GET', self.url('app', (slug or id,)))
        return response

    def get_app_privacy(self, slug=None, id=None):
        """Get an app's privacy.
        """

        response = self.conn.fetch('GET', self.url('app_privacy',
                                                   (slug or id,)))
        return response

    def create_app(self, **kwargs):
        """Create a new app.
        """

        response = self.conn.fetch('POST', self.url('apps'), kwargs)
        return response

    def update_app(self, id, app):
        """Update app.
        """

        response = self.conn.fetch('PUT', self.url('app', (id,)), app)
        return response

    def get_categories(self):
        """Get all exisiting categories.
        """

        response = self.conn.fetch('GET', self.url('categories'))
        return response

    def add_preview(self, app_id, position, file_path, type):
        """Upload a screenshot or video for an app.
        """

        import base64, os
        preview_file = open(file_path)

        data = {
            'position': position,
            'file': {
                'type': type,
                'name': file_path,
                'data': base64.b64encode(preview_file.read()),
            },
        }
        response = self.conn.fetch('POST', '%s?app=%s' % (self.url('screenshot'), app_id), data)
        return response

    def change_app_status(self, app_id, status):
        """Change status of an app.
        """

        response = self.conn.fetch('PATCH', self.url('status', (app_id,)), dict(status=status))
        return response
