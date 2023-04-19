from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _


User = get_user_model()


class Course(models.Model):

    teacher = models.ForeignKey(User, on_delete=models.PROTECT, related_name='courses')

    name = models.CharField(_('name'), max_length=255)

    is_archived = models.BooleanField(_('is archived'), default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
