import logging

from .tasks import send_email_post


logger = logging.getLogger(__name__)


def signal_send_email_post(sender, instance, created, **kwargs):
    if instance.is_sent:
        send_email_post(instance)
    else:
        logger.debug(f'Post with id {instance.id} already sent')
