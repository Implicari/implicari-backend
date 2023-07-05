from django.contrib.auth import get_user_model
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import Client
from django.test import override_settings

from implicari.apps.courses.models import Course

from .models import Message
from .tasks import send_email_message


User = get_user_model()


class TasksTestCase(StaticLiveServerTestCase):
    fixtures = [
        'fixtures/users.fake.json',
        'fixtures/courses.fake.json',
        'fixtures/posts.fake.json',
    ]

    def test_send_email_post_success(self):
        from django.core import mail

        total_emails = len(mail.outbox)

        post = Message.objects.last()
        parents = User.objects.distinct().filter(
            students__courses=post.course,
        )

        send_email_message(post)

        self.assertEqual(len(mail.outbox) - total_emails, parents.count())

    @override_settings(EMAIL_BACKEND=None)
    def test_send_email_post_fail(self):
        from django.core import mail

        total_emails = len(mail.outbox)

        with self.assertRaises(Exception):
            send_email_message(Message.objects.last())

        self.assertEqual(len(mail.outbox), total_emails)


class MessageListViewTestCase(StaticLiveServerTestCase):
    fixtures = [
        'fixtures/users.fake.json',
        'fixtures/courses.fake.json',
    ]

    def test_get(self):
        client = Client()
        client.force_login(User.objects.get(email='saul.hormazabal@gmail.com'))
        response = client.get('/cursos/1/mensajes/', secure=True)

        self.assertEqual(response.status_code, 200)


class MessageCreateViewTestCase(StaticLiveServerTestCase):
    fixtures = [
        'fixtures/users.fake.json',
        'fixtures/courses.fake.json',
    ]

    def test_get(self):
        client = Client()
        client.force_login(User.objects.get(email='saul.hormazabal@gmail.com'))
        response = client.get('/cursos/1/mensajes/crear/', secure=True)

        self.assertEqual(response.status_code, 200)

    def test_post(self):
        user = User.objects.get(email='saul.hormazabal@gmail.com')

        client = Client()
        client.force_login(user)

        self.assertTrue(not Message.objects.exists())

        data = {
            'subject': 'Lorem',
            'message': 'Ipsum',
        }

        response = client.post('/cursos/1/mensajes/crear/', data, secure=True)

        self.assertEqual(Message.objects.count(), 1)

        self.assertRedirects(
            response,
            f'/cursos/1/mensajes/{Message.objects.get().id}/',
            fetch_redirect_response=False,
        )


class MessageDetailViewTestCase(StaticLiveServerTestCase):
    fixtures = [
        'fixtures/users.fake.json',
        'fixtures/courses.fake.json',
        'fixtures/posts.fake.json',
    ]

    def test_get(self):
        client = Client()
        client.force_login(User.objects.get(email='saul.hormazabal@gmail.com'))
        response = client.get('/cursos/1/mensajes/1/', secure=True)

        self.assertEqual(response.status_code, 200)

    def test_dispatch_no_permission(self):
        email = 'saul.hormazabal@gmail.com'

        client = Client()
        client.force_login(User.objects.get(email=email))

        course = Course.objects.create(
            creator=User.objects.exclude(email=email).first(),
            name='Lorem Ipsum',
        )

        response = client.get(f'/cursos/{course.id}/mensajes/1/', secure=True)

        self.assertEqual(response.status_code, 403)


class MessageModelTestCase(StaticLiveServerTestCase):
    fixtures = [
        'fixtures/users.fake.json',
        'fixtures/courses.fake.json',
        'fixtures/posts.fake.json',
    ]

    def test_pending_manager(self):
        Message.objects.filter(id=1).update(is_sent=False)

        posts = Message.objects.all()
        posts_pendings = Message.pendings.all()
        posts_completed = posts.exclude(id__in=posts_pendings)

        self.assertTrue(posts.exists())
        self.assertTrue(posts_pendings.exists())
        self.assertTrue(posts_completed.exists())

        self.assertEqual(posts.count(), posts_pendings.count() + posts_completed.count())

        for post in posts_pendings:
            self.assertFalse(post.is_sent)

        for post in posts_completed:
            self.assertTrue(post.is_sent)

    def test_to_string(self):
        post = Message.objects.first()

        course = post.course

        self.assertIsNotNone(post.__str__())
        self.assertNotEqual(post.__str__(), "")
        self.assertIn(course.name, post.__str__())
        self.assertIn(post.subject, post.__str__())
