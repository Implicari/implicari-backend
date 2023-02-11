from django.contrib.auth import get_user_model
from django_better_admin_arrayfield.models.fields import ArrayField
from django.db import models
from django.db.models.signals import post_save

from implicari.apps.courses.models import Course

from .signals import signal_send_email_post


User = get_user_model()


class Post(models.Model):
    creator = models.ForeignKey(
        to=User,
        related_name='posts',
        on_delete=models.DO_NOTHING,
    )
    course = models.ForeignKey(
        to=Course,
        related_name='posts',
        on_delete=models.CASCADE,
    )

    subject = models.CharField(max_length=255)
    message = models.TextField()

    files = ArrayField(models.FileField())

    is_sent = models.BooleanField(default=False)

    creation_timestamp = models.DateTimeField(auto_now_add=True)
    update_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.classroom}: {self.subject}'


post_save.connect(signal_send_email_post, sender=Post)
