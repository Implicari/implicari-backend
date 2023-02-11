from django.db import models
from django.contrib.auth import get_user_model

from implicari.apps.courses.models import Course


User = get_user_model()


class AbstractPerson(models.Model):
    run = models.CharField(max_length=255)

    first_name = models.CharField('nombres', max_length=150)
    last_name = models.CharField('apellidos', max_length=150)

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Parent(AbstractPerson):
    user = models.ForeignKey(
        to=User,
        related_name='parents',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        verbose_name = 'apoderado'
        verbose_name_plural = 'apoderados'


class Student(AbstractPerson):
    course = models.ForeignKey(
        Course,
        related_name='students',
        on_delete=models.CASCADE,
    )

    user = models.ForeignKey(
        to=User,
        related_name='students',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    parents = models.ManyToManyField(
        'Parent',
        blank=True,
        related_name='students',
    )

    class Meta:
        verbose_name = 'estudiante'
        verbose_name_plural = 'estudiantes'
        unique_together = (
            'course',
            'run',
        )
