from django.contrib.auth import get_user_model
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import Client

from classrooms.models import Classroom

from .tasks import send_email_parent_invitation


User = get_user_model()


class TasksTestCase(StaticLiveServerTestCase):
    fixtures = [
        'fixtures/users.fake.json',
        'fixtures/classrooms.fake.json',
        'fixtures/posts.fake.json',
    ]

    def test_send_email_parent_invitation(self):

        classroom = Classroom.objects.get()
        student = classroom.students.first()
        parent = student.parents.first()

        password = 'test123456'
        base_url = 'http://test/'

        send_email_parent_invitation(
            parent=parent,
            classroom=classroom,
            student=student,
            password=password,
            base_url=base_url,
        )


class ParentCreateViewTestCase(StaticLiveServerTestCase):
    fixtures = [
        'fixtures/users.fake.json',
        'fixtures/classrooms.fake.json',
    ]

    def test_get(self):
        client = Client()
        client.force_login(User.objects.get(email='saul.hormazabal@gmail.com'))
        response = client.get('/cursos/1/estudiantes/2/apoderados/crear/', secure=True)

        self.assertEqual(response.status_code, 200)


class ParentDetailViewTestCase(StaticLiveServerTestCase):
    fixtures = [
        'fixtures/users.fake.json',
        'fixtures/classrooms.fake.json',
    ]

    def test_get(self):
        client = Client()
        client.force_login(User.objects.get(email='saul.hormazabal@gmail.com'))
        response = client.get('/cursos/1/estudiantes/2/apoderados/1/', secure=True)

        self.assertEqual(response.status_code, 200)
