from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save

from implicari.apps.communications.signals import signal_send_message


User = get_user_model()


class Message(models.Model):
    course = models.ForeignKey('courses.Course', related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.PROTECT)

    subject = models.CharField(max_length=100)
    body = models.TextField()

    is_email_sent = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'mensaje'
        verbose_name_plural = 'mensajes'


post_save.connect(signal_send_message, sender=Message)