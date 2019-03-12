from .tasks import send_email_question


def signal_send_email_question(sender, instance, created, **kwargs):
    if created:
        send_email_question(instance)
    else:
        pass
