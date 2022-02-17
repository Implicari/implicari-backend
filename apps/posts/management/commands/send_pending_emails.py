from django.core.management.base import BaseCommand

from posts.tasks import send_email_post
from posts.models import Post


class Command(BaseCommand):
    help = 'Send emails that not sent when was created'

    def handle(self, *args, **options):

        for post in Post.pendings.all():
            self.stdout.write('Sending "%s"' % post)
            send_email_post(post)

        self.stdout.write(self.style.SUCCESS('Successfully sent emails'))
