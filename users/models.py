from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    parents = models.ManyToManyField('self', blank=True, related_name='students', symmetrical=False)

    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    email = models.EmailField(_('email address'), null=True, unique=True, blank=True)

    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __repr__(self):
        return f'<{self.__class__.__name__}: {self.email or self.id}>'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def save(self, *args, **kwargs):
        self.email = self.email if self.email else None

        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return self.get_update_url()

    def get_update_url(self):
        return reverse('user-update', kwargs={'pk': self.pk})
