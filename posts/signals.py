from .tasks import send_email_post


def signal_send_email_post(sender, instance, created, **kwargs):
    if created:
        send_email_post(instance)
    else:
        pass
