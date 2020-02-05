from .tasks import send_email_event


def signal_send_email_event(sender, instance, created, **kwargs):
    if created:
        send_email_event(instance)
