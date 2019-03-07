from django.core import mail
from django.template.loader import render_to_string

from html2text import html2text

from users.models import User


def send_email_post(post):
    try:
        parents = User.objects.distinct().filter(
            students__classrooms=post.classroom,
            email__isnull=False,
        )

        messages = []
        subject = f'{post.classroom}: {post.subject}'
        content_html = render_to_string('posts/post_email.html', {'post': post})
        content_text = html2text(post.message.replace('<p><br></p>', ''))

        for parent in parents:
            message = mail.EmailMultiAlternatives(
                subject,
                content_text,
                post.creator.email,
                [parent.email],
            )
            message.attach_alternative(content_html, 'text/html')
            messages.append(message)

        connection = mail.get_connection(fail_silently=False)
        connection.send_messages(messages)

        post.is_sent = True
        post.save()

    except Exception as e:
        post.is_sent = False
        post.save()

        raise e
