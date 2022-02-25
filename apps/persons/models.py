from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Person(models.Model):
    id = models.AutoField(primary_key=True)

    user = models.ForeignKey(
        to=User,
        related_name='persons',
        null=True,
        on_delete=models.SET_NULL,
    )

    classroom = models.ForeignKey(
        to='classrooms.Classroom',
        related_name='students',
        on_delete=models.CASCADE,
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
