from django.db import models
from django.utils.translation import gettext as _


class Course(models.Model):

    name = models.CharField(_('name'), max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
