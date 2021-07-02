from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.urls import reverse
from django.utils.translation import gettext as _

from classrooms.models import Classroom

from .signals import signal_send_email_question


User = get_user_model()


class QuestionManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()


class QuestionPendingManager(QuestionManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_sent=False)


class Question(models.Model):
    id = models.AutoField(primary_key=True)

    creator = models.ForeignKey(User, related_name='questions', on_delete=models.DO_NOTHING)
    classroom = models.ForeignKey(Classroom, related_name='questions', on_delete=models.CASCADE)

    subject = models.CharField(_('asunto'), max_length=255)
    message = models.TextField(_('mensaje'))

    is_sent = models.BooleanField(default=False)

    creation_timestamp = models.DateTimeField(_('creation timestamp'), auto_now_add=True)
    update_timestamp = models.DateTimeField(_('update timestamp'), auto_now=True)

    objects = QuestionManager()
    pendings = QuestionPendingManager()

    class Meta:
        ordering = (
            'creation_timestamp',
        )

    def __str__(self):
        return f'{self.classroom}: {self.subject}'

    def get_detail_url(self):
        return reverse('question-detail', kwargs={'classroom_pk': self.classroom_id, 'pk': self.pk})


class Answer(models.Model):
    id = models.AutoField(primary_key=True)

    creator = models.ForeignKey(User, related_name='answers', on_delete=models.DO_NOTHING)
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)

    message = models.TextField(_('mensaje'))

    is_sent = models.BooleanField(default=False)

    creation_timestamp = models.DateTimeField(_('creation timestamp'), auto_now_add=True)
    update_timestamp = models.DateTimeField(_('update timestamp'), auto_now=True)

    class Meta:
        ordering = (
            'creation_timestamp',
        )

    def __str__(self):
        return f'{self.question}: {self.message}'


post_save.connect(signal_send_email_question, sender=Question)
