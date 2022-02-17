from django.core import mail
from django.template.loader import render_to_string

from html2text import html2text

from users.models import User


def send_email_question(question):
    try:
        parents = User.objects.distinct().filter(
            students__classrooms=question.classroom,
            email__isnull=False,
        )

        messages = []
        subject = f'{question.classroom}: {question.subject}'
        content_html = render_to_string('questions/question_email.html', {'question': question})
        content_text = html2text(question.message.replace('<p><br></p>', ''))

        for parent in parents:
            message = mail.EmailMultiAlternatives(
                subject,
                content_text,
                question.creator.email,
                [parent.email],
            )
            message.attach_alternative(content_html, 'text/html')
            messages.append(message)

        connection = mail.get_connection(fail_silently=False)
        connection.send_messages(messages)

        question.is_sent = True
        question.save()

    except Exception as e:
        question.is_sent = False
        question.save()

        raise e
