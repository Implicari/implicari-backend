from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.urls import reverse
from django.utils.translation import gettext as _

from classrooms.models import Classroom

from .signals import signal_send_email_post


User = get_user_model()


class PostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()


class PostPendingManager(PostManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_sent=False)


class Post(models.Model):
    creator = models.ForeignKey(User, related_name='posts', on_delete=models.DO_NOTHING)
    classroom = models.ForeignKey(Classroom, related_name='posts', on_delete=models.CASCADE)

    subject = models.CharField(max_length=255)
    message = models.TextField()

    is_sent = models.BooleanField(default=False)

    creation_timestamp = models.DateTimeField(_('creation timestamp'), auto_now_add=True)
    update_timestamp = models.DateTimeField(_('update timestamp'), auto_now=True)

    objects = PostManager()
    pendings = PostPendingManager()

    def __str__(self):
        return f'{self.classroom}: {self.subject}'

    def get_absolute_url(self):
        return self.get_update_url()

    def get_delete_url(self):
        return reverse('post-delete', kwargs={'classroom_pk': self.classroom_id, 'pk': self.pk})

    def get_detail_url(self):
        return reverse('post-detail', kwargs={'classroom_pk': self.classroom_id, 'pk': self.pk})

    def get_list_url(self):
        return reverse('post-list', kwargs={'classroom_pk': self.classroom_id})

    def get_update_url(self):
        return reverse('post-update', kwargs={'classroom_pk': self.classroom_id, 'pk': self.pk})


post_save.connect(signal_send_email_post, sender=Post)
