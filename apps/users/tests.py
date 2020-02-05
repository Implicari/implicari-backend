from django.contrib.auth import get_user_model
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import Client

from classrooms.models import Classroom


User = get_user_model()


class SignupTestCase(StaticLiveServerTestCase):

    def test_render_get(self):
        client = Client()
        response = client.get('/signup/', follow=True, secure=True)

        self.assertEqual(response.status_code, 200)

    def test_render_post_success(self):
        client = Client()

        email = 'test@test.com'

        data = {
            'email': email,
            'password1': 'test123456',
            'password2': 'test123456',
        }

        response = client.post('/signup/', data, secure=True)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/cursos/crear/')

        assert User.objects.filter(email=email).exists()

    def test_render_post_fail(self):
        client = Client()

        email = ''

        data = {
            'email': email,
            'password1': 'test123456',
            'password2': 'asd',
        }

        response = client.post('/signup/', data, secure=True)

        self.assertEqual(response.status_code, 200)

        assert not User.objects.filter(email=email).exists()


class ProfileUpdateViewTestCase(StaticLiveServerTestCase):
    fixtures = [
        'fixtures/users.fake.json',
    ]

    def test_get(self):
        client = Client()
        client.force_login(User.objects.get(email='saul.hormazabal@gmail.com'))
        response = client.get('/perfil/', secure=True)

        self.assertEqual(response.status_code, 200)

    def _post(self, email):
        first_name = 'qwe'
        last_name = 'asd'

        user = User.objects.get(email=email)

        assert user.first_name != first_name
        assert user.last_name != last_name

        client = Client()
        client.force_login(User.objects.get(email=email))

        data = {
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
        }

        response = client.post('/perfil/', data, secure=True)

        user.refresh_from_db()

        self.assertEqual(user.first_name, first_name)
        self.assertEqual(user.last_name, last_name)

        return response

    def test_post_with_zero_classroom(self):
        email = 'saul.hormazabal@gmail.com'
        user = User.objects.get(email=email)

        self.assertEqual(user.owner_classrooms.count(), 0)

        response = self._post(email)

        self.assertRedirects(response, '/cursos/crear/', fetch_redirect_response=False)

    def test_post_with_one_classroom(self):
        email = 'saul.hormazabal@gmail.com'
        user = User.objects.get(email=email)

        classroom = Classroom.objects.create(creator=user, name="Lorem")

        self.assertEqual(user.owner_classrooms.count(), 1)

        response = self._post(email)

        self.assertRedirects(response, f'/cursos/{classroom.id}/', fetch_redirect_response=False)

    def test_post_with_two_classroom(self):
        email = 'saul.hormazabal@gmail.com'
        user = User.objects.get(email=email)

        Classroom.objects.create(creator=user, name="Lorem")
        Classroom.objects.create(creator=user, name="Ipsum")

        self.assertEqual(user.owner_classrooms.count(), 2)

        response = self._post(email)

        self.assertRedirects(response, '/cursos/', fetch_redirect_response=False)
