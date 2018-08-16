from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _


User = get_user_model()


class Classroom(models.Model):
    creator = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name='owner_classrooms',
        verbose_name=_('creator'),
    )
    students = models.ManyToManyField(
        User,
        related_name='classrooms',
        verbose_name=_('creator'),
        blank=True,
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
        return self.get_update_url()

    def get_delete_url(self):
        return reverse('classroom-delete', kwargs={'pk': self.pk})

    def get_detail_url(self):
        return reverse('classroom-detail', kwargs={'pk': self.pk})

    def get_list_url(self):
        return reverse('classroom-list')

    def get_update_url(self):
        return reverse('classroom-update', kwargs={'pk': self.pk})

    def get_student_list_url(self):
        return reverse('student-list', kwargs={'classroom_pk': self.id})

    def get_student_create_url(self):
        return reverse('student-create', kwargs={'classroom_pk': self.id})
