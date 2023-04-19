from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.urls import reverse
from django.utils.translation import gettext as _

from implicari.apps.courses.models import Course

from .signals import signal_send_email_event


User = get_user_model()


class Event(models.Model):
    id = models.AutoField(primary_key=True)

    creator = models.ForeignKey(User, related_name='events', on_delete=models.DO_NOTHING)
    course = models.ForeignKey(Course, related_name='events', on_delete=models.CASCADE)

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    date = models.DateField(_('date'))
    time = models.TimeField(_('time'), null=True, blank=True)
    canceled = models.BooleanField(_('canceled'), default=False)

    creation_timestamp = models.DateTimeField(_('creation timestamp'), auto_now_add=True)
    update_timestamp = models.DateTimeField(_('update timestamp'), auto_now=True)

    class Meta:
        ordering = (
            'date',
        )

    def __str__(self):
        return f'{self.course}: {self.name}'


post_save.connect(signal_send_email_event, sender=Event)
