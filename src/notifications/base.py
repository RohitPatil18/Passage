from django.conf import settings
from django.core.mail.message import EmailMessage
from django.template.loader import render_to_string
from django.utils import timezone

from accounts.models import User
from notifications.models import EmailLog, NotificationLog


class BaseNotification:
    def __init__(self, event, recepients, context={}):
        self.event = event
        self.context = self.get_context(context)
        self.recepients = recepients

    def get_context(self, context):
        return context

    def check_notification_medium(self, medium):
        medium_config = self.event.get(medium)
        assert medium_config, f"{medium} configuration not added. Event: {self.event}"
        return medium_config.get("status", False)

    def relay_notification(self, notification, medium):
        if not self.check_notification_medium(medium):
            return
        from notifications import tasks

        if medium == "email":
            func = tasks.send_email_notification
        elif medium == "sms":
            func = tasks.send_sms_notification
        elif medium == "app_notification":
            func = tasks.send_in_app_notification
        if settings.NOTIFICATION_ASYNC:
            func.delay(notification, self.event[medium], self.recepients, self.context)
        else:
            func(notification, self.event[medium], self.recepients, self.context)

    def send_notification(self):
        notification = NotificationLog.objects.create(name=self.event["name"])
        for medium in {"email", "sms", "app_notification"}:
            self.relay_notification(notification, medium)


class BaseMail:
    subject = None
    template_path = None
    cc = []
    bcc = []

    def __init__(self, notification, config, recepients, context=None):
        self.notification = notification
        self.config = config
        self.context = context
        self.recepients = recepients

    def get_context(self, **kwargs):
        return self.context

    def get_subject(self):
        assert self.subject, (
            "'%s' should either include a `subject` attribute, "
            "or override the `get_subject()` method." % self.__class__.__name__
        )
        return self.subject

    def get_email_body(self, context):
        assert self.template_path, (
            "'%s' should either include a `template_path` attribute, "
            "or override the `get_email_body()` method." % self.__class__.__name__
        )
        return render_to_string(self.template_path, context)

    def get_cc(self):
        return self.cc

    def get_bcc(self):
        return self.bcc

    def get_recepients(self):
        recepients = self.recepients
        if isinstance(recepients, list):
            recepients = [r.email_address for r in recepients]
        elif isinstance(recepients, User):
            recepients = [recepients.email_address]
        return recepients

    def send_email(self):
        context = self.get_context()

        dataset = {
            "subject": self.get_subject(),
            "body": self.get_email_body(context),
            "recepients": self.get_recepients(),
            "cc": self.get_cc(),
            "bcc": self.get_bcc(),
        }

        log = EmailLog.objects.create(**dataset, notification=self.notification)
        self.notification.email_log = log
        self.notification.save()

        try:
            dataset["to"] = dataset.pop("recepients")
            email = EmailMessage(
                **dataset,
                from_email=settings.EMAIL_FROM,
            )
            email.content_subtype = "html"
            email.send()
            log.is_sent = True
            log.sent_at = timezone.now()
            log.save(update_fields=["is_sent", "sent_at"])
        except Exception as e:
            """
            Email failure status will be stored in email log table
            """
            log.failure_reason = str(e)
            log.save(update_fields=["failure_reason"])
