from django.contrib.auth import get_user_model
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import Client

from classrooms.models import Classroom


User = get_user_model()


class ClassroomListViewTestCase(StaticLiveServerTestCase):
    fixtures = [
        'fixtures/users.fake.json',
    ]

    def test_get(self):
        client = Client()
        client.force_login(User.objects.get(email='saul.hormazabal@gmail.com'))
        response = client.get('/cursos/', secure=True)

        self.assertEqual(response.status_code, 200)


class ClassroomCreateViewTestCase(StaticLiveServerTestCase):
    fixtures = [
        'fixtures/users.fake.json',
    ]

    def test_get(self):
        client = Client()
        client.force_login(User.objects.get(email='saul.hormazabal@gmail.com'))
        response = client.get('/cursos/crear/', secure=True)

        self.assertEqual(response.status_code, 200)

    def test_post(self):
        user = User.objects.get(email='saul.hormazabal@gmail.com')

        client = Client()
        client.force_login(user)

        self.assertFalse(Classroom.objects.exists())

        data = {
            'name': 'Lorem',
        }

        response = client.post(f'/cursos/crear/', data, secure=True)

        self.assertTrue(Classroom.objects.exists())
        self.assertRedirects(response, f'/cursos/', fetch_redirect_response=False)


class ClassroomDeleteViewTestCase(StaticLiveServerTestCase):
    fixtures = [
        'fixtures/users.fake.json',
        'fixtures/classrooms.fake.json',
    ]

    def test_get(self):
        client = Client()
        client.force_login(User.objects.get(email='saul.hormazabal@gmail.com'))
        response = client.get('/cursos/1/eliminar/', secure=True)

        self.assertEqual(response.status_code, 200)


class ClassroomDetailViewTestCase(StaticLiveServerTestCase):
    fixtures = [
        'fixtures/users.fake.json',
        'fixtures/classrooms.fake.json',
    ]

    def test_get(self):
        client = Client()
        client.force_login(User.objects.get(email='saul.hormazabal@gmail.com'))
        response = client.get('/cursos/1/', secure=True)

        self.assertEqual(response.status_code, 200)


class ClassroomUpdateViewTestCase(StaticLiveServerTestCase):
    fixtures = [
        'fixtures/users.fake.json',
        'fixtures/classrooms.fake.json',
    ]

    def test_get(self):
        client = Client()
        client.force_login(User.objects.get(email='saul.hormazabal@gmail.com'))
        response = client.get('/cursos/1/editar/', secure=True)

        self.assertEqual(response.status_code, 200)
