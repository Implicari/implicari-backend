from django.contrib.auth import get_user_model
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.db.models import Q
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

        response = client.post('/cursos/crear/', data, secure=True)

        self.assertTrue(Classroom.objects.exists())
        self.assertRedirects(response, '/cursos/', fetch_redirect_response=False)


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

    def test_post(self):
        user = User.objects.get(email='saul.hormazabal@gmail.com')
        classroom = Classroom.objects.first()

        client = Client()
        client.force_login(user)

        data = {
        }

        response = client.post(classroom.get_delete_url(), data, secure=True)

        self.assertFalse(Classroom.objects.filter(id=classroom.id).exists())
        self.assertRedirects(response, '/cursos/', fetch_redirect_response=False)


class ClassroomDetailViewTestCase(StaticLiveServerTestCase):
    fixtures = [
        'fixtures/users.fake.json',
        'fixtures/classrooms.fake.json',
    ]

    def test_get_as_teacher(self):
        client = Client()
        client.force_login(User.objects.get(id=1))
        response = client.get('/cursos/1/', secure=True)

        self.assertEqual(response.status_code, 200)

    def test_get_as_student(self):
        client = Client()
        client.force_login(User.objects.get(id=2))
        response = client.get('/cursos/1/', secure=True)

        self.assertEqual(response.status_code, 200)

    def test_get_as_parent(self):
        client = Client()
        client.force_login(User.objects.get(id=3))
        response = client.get('/cursos/1/', secure=True)

        self.assertEqual(response.status_code, 200)

    def test_get_handle_no_permission(self):
        classroom = Classroom.objects.first()
        user = User.objects.exclude(
            Q(classrooms=classroom) |
            Q(students__classrooms=classroom) |
            Q(parents__students__classrooms=classroom)
        ).first()

        client = Client()
        client.force_login(user)
        response = client.get(f'/cursos/{classroom.id}/', secure=True)

        self.assertEqual(response.status_code, 403)


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

    def test_post(self):
        user = User.objects.get(email='saul.hormazabal@gmail.com')
        classroom = Classroom.objects.first()

        client = Client()
        client.force_login(user)

        name = 'Lorem'

        self.assertNotEqual(classroom.name, name)

        data = {
            'name': name,
        }

        response = client.post(f'/cursos/{classroom.id}/editar/', data, secure=True)

        classroom.refresh_from_db()

        self.assertRedirects(response, f'/cursos/{classroom.id}/', fetch_redirect_response=False)
        self.assertEqual(classroom.name, name)
