from django.contrib.auth import get_user_model
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.db.models import Q
from django.test import Client
from django.test import override_settings

from classrooms.models import Classroom

from .models import Answer
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

    def test_post_answer(self):
        user = User.objects.get(email='saul.hormazabal@gmail.com')

        question = Question.objects.first()
        classroom = question.classroom

        client = Client()
        client.force_login(user)

        self.assertFalse(Answer.objects.exists())

        data = {
            'subject': 'Lorem',
            'message': 'Ipsum',
        }

        url = f'/cursos/{classroom.id}/preguntas/{question.id}/'
        response = client.post(url, data, secure=True)

        self.assertTrue(Answer.objects.exists())

        self.assertRedirects(
            response,
            f'/cursos/{classroom.id}/preguntas/{question.id}/',
            fetch_redirect_response=False,
        )

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


class QuestionModelTestCase(StaticLiveServerTestCase):
    fixtures = [
        'fixtures/users.fake.json',
        'fixtures/classrooms.fake.json',
        'fixtures/questions.fake.json',
    ]

    def test_pending_manager(self):
        Question.objects.filter(id=1).update(is_sent=False)

        questions = Question.objects.all()
        questions_pendings = Question.pendings.all()
        questions_completed = questions.exclude(id__in=questions_pendings)

        self.assertTrue(questions.exists())
        self.assertTrue(questions_pendings.exists())
        self.assertTrue(questions_completed.exists())

        total_pendings_completed = questions_pendings.count() + questions_completed.count()
        self.assertEqual(questions.count(), total_pendings_completed)

        for question in questions_pendings:
            self.assertFalse(question.is_sent)

        for question in questions_completed:
            self.assertTrue(question.is_sent)
