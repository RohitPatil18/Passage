from uuid import uuid4

from django.conf import settings

from accounts.models import PasswordResetCode
from notifications.base import BaseMail, BaseNotification


class PasswordResetLinkNotification(BaseNotification):
    def get_context(self, context):
        resetcode = PasswordResetCode.objects.create(
            code=uuid4().hex, user_id=context["user_id"]
        )
        context[
            "password_reset_link"
        ] = f"{settings.RESET_PASSWORD_URL}?code={resetcode.code}"
        return context


class PasswordResetLinkMail(BaseMail):
    subject = "Forgot password? Reset using following link."
    template_path = "notifications/emails/password_reset_link_mail.html"
