from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import Client


class IndexTestCase(StaticLiveServerTestCase):
    fixtures = [
        'fixtures/users',
    ]

    def test_render_landing_when_unauthenticated(self):
        client = Client()
        response = client.get('/')

        self.assertEqual(response.status_code, 200)
