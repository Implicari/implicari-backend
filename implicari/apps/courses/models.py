from django.db import models
from django.utils.translation import gettext as _

from implicari.apps.schools.models import School


class Course(models.Model):

    school = models.ForeignKey(
        School,
        related_name='courses',
        on_delete=models.PROTECT,
    )

    name = models.CharField(_('name'), max_length=255)

    def __str__(self):
        return f'{self.name} {self.school}'
