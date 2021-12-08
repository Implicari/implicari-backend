from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _

from persons.models import Person


User = get_user_model()


class Classroom(models.Model):
    id = models.AutoField(primary_key=True)

    creator = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name='owner_classrooms',
        verbose_name=_('creator'),
    )
    name = models.CharField(_('name'), max_length=255)
    is_archived = models.BooleanField(_('is archived'), default=False)

    creation_timestamp = models.DateTimeField(_('creation timestamp'), auto_now_add=True)
    update_timestamp = models.DateTimeField(_('update timestamp'), auto_now=True)

    class Meta:
        verbose_name_plural = 'classrooms'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return self.get_detail_url()

    def get_delete_url(self):
        return reverse('classroom-delete', kwargs={'pk': self.pk})

    def get_detail_url(self):
        return reverse('classroom-detail', kwargs={'pk': self.pk})

    def get_list_url(self):
        return reverse('classroom-list')

    def get_update_url(self):
        return reverse('classroom-update', kwargs={'pk': self.pk})

    def get_student_list_url(self):
        return reverse('classroom-detail', kwargs={'pk': self.id})

    def get_post_list_url(self):
        return reverse('post-list', kwargs={'classroom_pk': self.id})

    def get_event_list_url(self):
        return reverse('event-list', kwargs={'classroom_pk': self.id})

    def get_question_list_url(self):
        return reverse('question-list', kwargs={'classroom_pk': self.id})
