from django.core import mail
from django.template.loader import render_to_string


def send_email_parent_invitation(parent, classroom, student, password, base_url):
    subject = f'Invitación a {classroom} como apoderado de {student}'
    content_context = {
        'parent': parent,
        'classroom': classroom,
        'student': student,
        'password': password,
        'base_url': base_url,
    }
    content_html = render_to_string('parents/parent_email_invitation.html', content_context)
    content_text = render_to_string('parents/parent_email_invitation.txt', content_context)

    message = mail.EmailMultiAlternatives(
        subject,
        content_text,
        parent.email,
        [parent.email],
    )
    message.attach_alternative(content_html, 'text/html')
    message.send()
