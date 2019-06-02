from django.contrib.auth import get_user_model
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import Client

from classrooms.models import Classroom
from events.models import Event

from .tasks import send_email_event


User = get_user_model()


class TasksTestCase(StaticLiveServerTestCase):
    fixtures = [
        'fixtures/users.fake.json',
        'fixtures/classrooms.fake.json',
        'fixtures/events.fake.json',
    ]

    def test_send_email_event_success(self):
        send_email_event(Event.objects.last())


class EventListViewTestCase(StaticLiveServerTestCase):
    fixtures = [
        'fixtures/users.fake.json',
        'fixtures/classrooms.fake.json',
    ]

    def test_get(self):
        client = Client()
        client.force_login(User.objects.get(email='saul.hormazabal@gmail.com'))
        response = client.get('/cursos/1/eventos/', secure=True)

        self.assertEqual(response.status_code, 200)


class EventCreateViewTestCase(StaticLiveServerTestCase):
    fixtures = [
        'fixtures/users.fake.json',
        'fixtures/classrooms.fake.json',
    ]

    def test_get(self):
        client = Client()
        client.force_login(User.objects.get(email='saul.hormazabal@gmail.com'))
        response = client.get('/cursos/1/eventos/crear/', secure=True)

        self.assertEqual(response.status_code, 200)

    def test_post(self):
        user = User.objects.get(email='saul.hormazabal@gmail.com')

        client = Client()
        client.force_login(user)

        classroom = Classroom.objects.first()

        self.assertFalse(Event.objects.exists())

        data = {
            'description': 'Lorem',
            'message': 'Ipsum',
            'date': '2019-06-01',
        }

        response = client.post(f'/cursos/{classroom.id}/eventos/crear/', data, secure=True)

        self.assertEqual(Event.objects.count(), 1)

        self.assertRedirects(
            response,
            f'/cursos/{classroom.id}/eventos/',
            fetch_redirect_response=False,
        )


class EventDetailViewTestCase(StaticLiveServerTestCase):
    fixtures = [
        'fixtures/users.fake.json',
        'fixtures/classrooms.fake.json',
        'fixtures/events.fake.json',
    ]

    def test_get(self):
        client = Client()
        client.force_login(User.objects.get(email='saul.hormazabal@gmail.com'))
        response = client.get('/cursos/1/eventos/1/', secure=True)

        self.assertEqual(response.status_code, 200)


class EventDeleteViewTestCase(StaticLiveServerTestCase):
    fixtures = [
        'fixtures/users.fake.json',
        'fixtures/classrooms.fake.json',
        'fixtures/events.fake.json',
    ]

    def test_get(self):
        client = Client()
        client.force_login(User.objects.get(email='saul.hormazabal@gmail.com'))
        response = client.get('/cursos/1/eventos/1/eliminar/', secure=True)

        self.assertEqual(response.status_code, 200)

    def test_post(self):
        user = User.objects.get(email='saul.hormazabal@gmail.com')
        event = Event.objects.first()
        classroom = event.classroom

        client = Client()
        client.force_login(user)

        data = {
        }

        response = client.post(event.get_delete_url(), data, secure=True)

        self.assertFalse(Event.objects.filter(id=event.id).exists())
        self.assertRedirects(
            response,
            f'/cursos/{classroom.id}/eventos/',
            fetch_redirect_response=False,
        )


class EventUpdateViewTestCase(StaticLiveServerTestCase):
    fixtures = [
        'fixtures/users.fake.json',
        'fixtures/classrooms.fake.json',
        'fixtures/events.fake.json',
    ]

    def test_get(self):
        client = Client()
        client.force_login(User.objects.get(email='saul.hormazabal@gmail.com'))
        response = client.get('/cursos/1/eventos/1/editar/', secure=True)

        self.assertEqual(response.status_code, 200)

    def test_post(self):
        user = User.objects.get(email='saul.hormazabal@gmail.com')
        event = Event.objects.first()
        classroom = event.classroom

        client = Client()
        client.force_login(user)

        description = 'Lorem'
        message = 'Ipsum'
        date = '2019-06-01'

        assert event.description != description
        assert event.message != message
        assert event.date.isoformat() != date

        data = {
            'description': description,
            'message': message,
            'date': date,
        }

        response = client.post(
            f'/cursos/{classroom.id}/eventos/{event.id}/editar/',
            data,
            secure=True,
        )

        event.refresh_from_db()

        self.assertRedirects(
            response,
            f'/cursos/{classroom.id}/eventos/',
            fetch_redirect_response=False,
        )

        self.assertEqual(event.description, description)
        self.assertEqual(event.message, message)
        self.assertEqual(event.date.isoformat(), date)


class EventModelTestCase(StaticLiveServerTestCase):
    fixtures = [
        'fixtures/users.fake.json',
        'fixtures/classrooms.fake.json',
        'fixtures/events.fake.json',
    ]

    def test_get_absolute_url(self):
        user = User.objects.get(email='saul.hormazabal@gmail.com')
        event = Event.objects.first()

        client = Client()
        client.force_login(user)

        response = client.get(event.get_absolute_url(), secure=True)

        self.assertEqual(response.status_code, 200)

    def test_to_string(self):
        event = Event.objects.first()

        classroom = event.classroom

        self.assertIsNotNone(event.__str__())
        self.assertNotEqual(event.__str__(), "")
        self.assertIn(classroom.name, event.__str__())
        self.assertIn(event.description, event.__str__())
