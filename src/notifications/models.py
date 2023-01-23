from django.db import models


class NotificationLog(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        db_table = "sys_notification_logs"


class EmailLog(models.Model):
    notification = models.ForeignKey(NotificationLog, on_delete=models.CASCADE)
    subject = models.TextField()
    body = models.TextField()
    recepients = models.JSONField()
    cc = models.JSONField(null=True)
    bcc = models.JSONField(null=True)
    is_sent = models.BooleanField(default=False)
    sent_at = models.DateTimeField(null=True)
    failure_reason = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "sys_email_logs"
