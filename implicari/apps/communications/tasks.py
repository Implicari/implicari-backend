from django.core import mail
from django.template.loader import render_to_string

from html2text import html2text
from implicari.apps.persons.models import Parent

from implicari.apps.users.models import User


def send_email_message(message):

    parents = Parent.objects.distinct().filter(
        students__course=message.course,
        user__isnull=False,
    )

    emails = []
    subject = f'{message.course}: {message.subject}'
    content_html = render_to_string('comunications/email.html', {'post': message})
    content_text = html2text(message.body.replace('<p><br></p>', ''))

    for parent in parents:
        email = mail.EmailMultiAlternatives(
            subject,
            content_text,
            message.sender.email,
            [parent.user.email],
        )
        email.attach_alternative(content_html, 'text/html')
        emails.append(email)

    connection = mail.get_connection(fail_silently=False)
    connection.send_messages(emails)

    message.is_email_sent = True
    message.save()