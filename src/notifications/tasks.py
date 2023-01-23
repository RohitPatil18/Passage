from celery import shared_task
from django.utils.module_loading import import_string

from notifications import base


def notify_user(event, recepients, context):
    script = event.get("script")
    if script:
        Notification = import_string(event["script"])
        notification = Notification(event, recepients, context)
    else:
        notification = base.BaseNotification(event, recepients, context)
    notification.send_notification()


@shared_task
def send_email_notification(notification, config, recepients, context):
    Mail = import_string(config["script"])
    Mail(notification, config, recepients, context).send_email()


@shared_task
def send_sms_notification(notification, config, recepients, context):
    """
    @TODO: Send SMS implemention
    """


@shared_task
def send_in_app_notification(notification, config, recepients, context):
    """
    @TODO: Send App notification implemention
    """
