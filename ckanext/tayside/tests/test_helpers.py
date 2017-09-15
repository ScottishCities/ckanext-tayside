from ckan.tests import helpers as test_helpers, factories
from ckan import plugins
from ckan.common import config

from ckanext.tayside import helpers as tayside_helpers


class ActionBase(object):
    @classmethod
    def setup_class(self):
        if not plugins.plugin_loaded('tayside'):
            plugins.load('tayside')

    def setup(self):
        test_helpers.reset_db()

    @classmethod
    def teardown_class(self):
        if plugins.plugin_loaded('tayside'):
            plugins.unload('tayside')


class TestHelpers(ActionBase):
    def test_get_groups(self):
        group1 = factories.Group()
        group2 = factories.Group()
        org = factories.Organization()

        dataset_required_fields = {
            'maintainer': 'Aleksandar',
            'maintainer_email': 'test@test.com',
            'author': 'Aleksandar',
            'author_email': 'test@test.com',
            'tag_string': 'test',
            'owner_org': org.get('id')
        }

        for i in range(1):
            dataset_required_fields.update({
                'groups': [{'id': group1.get('id')}]
            })
            dataset = factories.Dataset(**dataset_required_fields)

        for i in range(3):
            dataset_required_fields.update({
                'groups': [{'id': group2.get('id')}]
            })
            dataset = factories.Dataset(**dataset_required_fields)

        groups = tayside_helpers.get_groups()

        assert groups[0].get('id') == group2.get('id')
        assert groups[1].get('id') == group1.get('id')
        assert groups[0].get('package_count') > groups[1].get('package_count')

    def test_get_footer_logos(self):
        config['footer_logo_1_image_url'] = 'http://example.com/image.png'
        config['footer_logo_1_link_url'] = 'http://google.com'
        config['footer_logo_1_text'] = 'some text'

        logos = tayside_helpers.get_footer_logos()

        assert len(logos) == 1
        assert logos[0].get('logo_image_url') ==\
            config['footer_logo_1_image_url']
        assert logos[0].get('logo_link_url') ==\
            config['footer_logo_1_link_url']
        assert logos[0].get('logo_text') ==\
            config['footer_logo_1_text']
