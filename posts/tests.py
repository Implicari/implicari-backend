from django.contrib.auth import get_user_model
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import Client
from django.test import override_settings

from classrooms.models import Classroom

from .models import Post
from .tasks import send_email_post


User = get_user_model()


class TasksTestCase(StaticLiveServerTestCase):
    fixtures = [
        'fixtures/users.fake.json',
        'fixtures/classrooms.fake.json',
        'fixtures/posts.fake.json',
    ]

    def test_send_email_post_success(self):
        from django.core import mail

        total_emails = len(mail.outbox)

        post = Post.objects.last()
        parents = User.objects.distinct().filter(
            students__classrooms=post.classroom,
        )

        send_email_post(post)

        self.assertEqual(len(mail.outbox) - total_emails, parents.count())

    @override_settings(EMAIL_BACKEND=None)
    def test_send_email_post_fail(self):
        from django.core import mail

        total_emails = len(mail.outbox)

        with self.assertRaises(Exception):
            send_email_post(Post.objects.last())

        self.assertEqual(len(mail.outbox), total_emails)


class PostListViewTestCase(StaticLiveServerTestCase):
    fixtures = [
        'fixtures/users.fake.json',
        'fixtures/classrooms.fake.json',
    ]

    def test_get(self):
        client = Client()
        client.force_login(User.objects.get(email='saul.hormazabal@gmail.com'))
        response = client.get('/cursos/1/mensajes/', secure=True)

        self.assertEqual(response.status_code, 200)


class PostCreateViewTestCase(StaticLiveServerTestCase):
    fixtures = [
        'fixtures/users.fake.json',
        'fixtures/classrooms.fake.json',
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

        self.assertTrue(not Post.objects.exists())

        data = {
            'subject': 'Lorem',
            'message': 'Ipsum',
        }

        response = client.post('/cursos/1/mensajes/crear/', data, secure=True)

        self.assertEqual(Post.objects.count(), 1)

        self.assertRedirects(
            response,
            f'/cursos/1/mensajes/{Post.objects.get().id}/',
            fetch_redirect_response=False,
        )


class PostDetailViewTestCase(StaticLiveServerTestCase):
    fixtures = [
        'fixtures/users.fake.json',
        'fixtures/classrooms.fake.json',
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

        classroom = Classroom.objects.create(
            creator=User.objects.exclude(email=email).first(),
            name='Lorem Ipsum',
        )

        response = client.get(f'/cursos/{classroom.id}/mensajes/1/', secure=True)

        self.assertEqual(response.status_code, 403)
