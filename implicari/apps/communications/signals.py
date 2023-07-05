import logging

from .tasks import send_email_message


logger = logging.getLogger(__name__)


def signal_send_message(sender, instance, created, **kwargs):
    if not instance.is_email_sent:
        send_email_message(instance)
    else:
        logger.debug(f'Post with id {instance.id} already sent')
