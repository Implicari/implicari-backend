from django.db import models
from django.utils.translation import gettext as _


class Course(models.Model):
    name = models.CharField(_('name'), max_length=255)

    classrooms = models.ManyToManyField(
        'classrooms.Classroom',
        related_name='courses',
        verbose_name=_('classrooms'),
    )

    def __str__(self):
        return self.name
