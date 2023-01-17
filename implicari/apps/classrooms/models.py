from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Classroom(models.Model):
    creator = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name='owner_classrooms',
    )

    name = models.CharField(max_length=255)
    is_archived = models.BooleanField(default=False)

    creation_timestamp = models.DateTimeField(auto_now_add=True)
    update_timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'classrooms'

    def __str__(self):
        return self.name
