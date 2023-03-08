from django.core import mail
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model

from html2text import html2text


User = get_user_model()


def send_email_event(event):
    parents = User.objects.distinct().filter(
        students__classrooms=event.classroom,
        email__isnull=False,
    )

    messages = []
    description = f'{event.classroom}: {event.description} el {event.date}'
    content_html = render_to_string('events/event_email.html', {'event': event})
    content_text = html2text(event.message.replace('<p><br></p>', ''))

    for parent in parents:
        message = mail.EmailMultiAlternatives(
            description,
            content_text,
            event.creator.email,
            [parent.email],
        )
        message.attach_alternative(content_html, 'text/html')
        messages.append(message)

    connection = mail.get_connection()
    connection.send_messages(messages)
