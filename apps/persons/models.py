from django.db import models
from django.utils.translation import ugettext_lazy as _


class Person(models.Model):
    id = models.AutoField(primary_key=True)

    parents = models.ManyToManyField(
        'self',
        blank=True,
        related_name='children',
        symmetrical=False,
    )

    first_name = models.CharField(_('first name'), max_length=150)
    last_name = models.CharField(_('last name'), max_length=150)
    run = models.IntegerField('RUN', null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
