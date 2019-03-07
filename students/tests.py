from django.contrib.auth import get_user_model
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import Client

from classrooms.models import Classroom


User = get_user_model()


class StudentCreateViewTestCase(StaticLiveServerTestCase):
    fixtures = [
        'fixtures/users.fake.json',
        'fixtures/classrooms.fake.json',
    ]

    def test_get(self):
        client = Client()
        client.force_login(User.objects.get(email='saul.hormazabal@gmail.com'))
        response = client.get('/cursos/1/estudiantes/crear/', secure=True)

        self.assertEqual(response.status_code, 200)

    def test_post(self):
        user = User.objects.get(email='saul.hormazabal@gmail.com')

        client = Client()
        client.force_login(user)

        student_ids = list(user.students.values_list('id', flat=True))

        data = {
            'first_name': 'Lorem',
            'last_name': 'Ipsum',
        }

        response = client.post('/cursos/1/estudiantes/crear/', data, secure=True)

        student_created = User.objects.exclude(id__in=student_ids + [user.id]).get()

        self.assertRedirects(
            response,
            f'/cursos/1/estudiantes/{student_created.id}/',
            fetch_redirect_response=False,
        )


class StudentDetailViewTestCase(StaticLiveServerTestCase):
    fixtures = [
        'fixtures/users.fake.json',
        'fixtures/classrooms.fake.json',
    ]

    def test_get(self):
        client = Client()
        client.force_login(User.objects.get(email='saul.hormazabal@gmail.com'))
        response = client.get('/cursos/1/estudiantes/2/', secure=True)

        self.assertEqual(response.status_code, 200)

    def test_dispatch_no_permission(self):
        email = 'saul.hormazabal@gmail.com'

        client = Client()
        client.force_login(User.objects.get(email=email))

        classroom = Classroom.objects.create(
            creator=User.objects.exclude(email=email).first(),
            name='Lorem Ipsum',
        )

        response = client.get(f'/cursos/{classroom.id}/estudiantes/2/', secure=True)

        self.assertEqual(response.status_code, 403)


class StudentDeleteViewTestCase(StaticLiveServerTestCase):
    fixtures = [
        'fixtures/users.fake.json',
        'fixtures/classrooms.fake.json',
    ]

    def test_get(self):
        client = Client()
        client.force_login(User.objects.get(email='saul.hormazabal@gmail.com'))
        response = client.get('/cursos/1/estudiantes/2/eliminar/', secure=True)

        self.assertEqual(response.status_code, 200)

    def test_post(self):
        user = User.objects.get(email='saul.hormazabal@gmail.com')
        student = user.students.first()
        classroom = student.classrooms.first()

        client = Client()
        client.force_login(user)

        data = {

        }

        response = client.post(
            f'/cursos/{classroom.id}/estudiantes/{student.id}/eliminar/',
            data,
            secure=True,
        )

        self.assertRedirects(response, classroom.get_absolute_url(), fetch_redirect_response=False)
        self.assertTrue(not User.objects.filter(id=student.id).exists())


class StudentUpdateViewTestCase(StaticLiveServerTestCase):
    fixtures = [
        'fixtures/users.fake.json',
        'fixtures/classrooms.fake.json',
    ]

    def test_get(self):
        client = Client()
        client.force_login(User.objects.get(email='saul.hormazabal@gmail.com'))
        response = client.get('/cursos/1/estudiantes/2/editar/', secure=True)

        self.assertEqual(response.status_code, 200)

    def test_post(self):
        user = User.objects.get(email='saul.hormazabal@gmail.com')
        student = user.students.first()
        classroom = student.classrooms.first()

        client = Client()
        client.force_login(user)

        first_name = 'Lorem'
        last_name = 'Ipsum'

        assert student.first_name != first_name
        assert student.last_name != last_name

        data = {
            'first_name': first_name,
            'last_name': last_name,
        }

        response = client.post(
            f'/cursos/{classroom.id}/estudiantes/{student.id}/editar/',
            data,
            secure=True,
        )

        student.refresh_from_db()

        self.assertRedirects(
            response,
            f'/cursos/{classroom.id}/estudiantes/{student.id}/',
            fetch_redirect_response=False,
        )

        self.assertEqual(student.first_name, first_name)
        self.assertEqual(student.last_name, last_name)
