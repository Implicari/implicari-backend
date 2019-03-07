from django.contrib.auth import get_user_model
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import Client


User = get_user_model()


class IndexTestCase(StaticLiveServerTestCase):
    fixtures = [
        'fixtures/users',
    ]

    def test_render_landing_when_unauthenticated(self):
        client = Client()
        response = client.get('/', secure=True)

        self.assertEqual(response.status_code, 200)

    def test_render_landing_when_authenticated(self):
        client = Client()
        client.force_login(User.objects.get(email='saul.hormazabal@gmail.com'))
        response = client.get('/', secure=True)

        self.assertRedirects(response, '/cursos/', fetch_redirect_response=False)
