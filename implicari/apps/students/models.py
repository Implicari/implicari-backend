from django.db import models
from django.contrib.auth import get_user_model

from implicari.apps.courses.models import Course


User = get_user_model()


class Student(models.Model):
    user = models.ForeignKey(
        to=User,
        related_name='persons',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    course = models.ForeignKey(
        Course,
        related_name='students',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    parents = models.ManyToManyField(
        'self',
        blank=True,
        related_name='children',
        symmetrical=False,
    )

    first_name = models.CharField('first name', max_length=150)
    last_name = models.CharField('last name', max_length=150)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
