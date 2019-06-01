from django.contrib.auth import get_user_model
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.db.models import Q
from django.test import Client
from django.test import override_settings

from classrooms.models import Classroom

from .models import Question
from .tasks import send_email_question


User = get_user_model()


class TasksTestCase(StaticLiveServerTestCase):
    fixtures = [
        'fixtures/users.fake.json',
        'fixtures/classrooms.fake.json',
        'fixtures/questions.fake.json',
    ]

    def test_send_email_post_success(self):
        from django.core import mail

        total_emails = len(mail.outbox)

        question = Question.objects.last()
        parents = User.objects.distinct().filter(
            students__classrooms=question.classroom,
        )

        send_email_question(question)

        self.assertEqual(len(mail.outbox) - total_emails, parents.count())

    @override_settings(EMAIL_BACKEND=None)
    def test_send_email_post_fail(self):
        from django.core import mail

        total_emails = len(mail.outbox)

        with self.assertRaises(Exception):
            send_email_question(Question.objects.last())

        self.assertEqual(len(mail.outbox), total_emails)


class QuestionListViewTestCase(StaticLiveServerTestCase):
    fixtures = [
        'fixtures/users.fake.json',
        'fixtures/classrooms.fake.json',
    ]

    def test_get(self):
        client = Client()
        client.force_login(User.objects.get(email='saul.hormazabal@gmail.com'))
        response = client.get('/cursos/1/preguntas/', secure=True)

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
        response = client.get(f'/cursos/{classroom.id}/preguntas/', secure=True)

        self.assertEqual(response.status_code, 403)


class QuestionCreateViewTestCase(StaticLiveServerTestCase):
    fixtures = [
        'fixtures/users.fake.json',
        'fixtures/classrooms.fake.json',
    ]

    def test_get(self):
        client = Client()
        client.force_login(User.objects.get(email='saul.hormazabal@gmail.com'))
        response = client.get('/cursos/1/preguntas/crear/', secure=True)

        self.assertEqual(response.status_code, 200)

    def test_post(self):
        user = User.objects.get(email='saul.hormazabal@gmail.com')

        client = Client()
        client.force_login(user)

        self.assertTrue(not Question.objects.exists())

        data = {
            'subject': 'Lorem',
            'message': 'Ipsum',
        }

        response = client.post('/cursos/1/preguntas/crear/', data, secure=True)

        self.assertEqual(Question.objects.count(), 1)

        self.assertRedirects(
            response,
            f'/cursos/1/preguntas/{Question.objects.get().id}/',
            fetch_redirect_response=False,
        )


class QuestionDetailViewTestCase(StaticLiveServerTestCase):
    fixtures = [
        'fixtures/users.fake.json',
        'fixtures/classrooms.fake.json',
        'fixtures/questions.fake.json',
    ]

    def test_get(self):
        client = Client()
        client.force_login(User.objects.get(email='saul.hormazabal@gmail.com'))
        response = client.get('/cursos/1/preguntas/1/', secure=True)

        self.assertEqual(response.status_code, 200)

    def test_dispatch_no_permission(self):
        email = 'saul.hormazabal@gmail.com'

        client = Client()
        client.force_login(User.objects.get(email=email))

        classroom = Classroom.objects.create(
            creator=User.objects.exclude(email=email).first(),
            name='Lorem Ipsum',
        )

        response = client.get(f'/cursos/{classroom.id}/preguntas/1/', secure=True)

        self.assertEqual(response.status_code, 403)
