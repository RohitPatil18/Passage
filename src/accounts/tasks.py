from uuid import uuid4

from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from accounts.models import PasswordResetCode


@shared_task
def send_password_reset_link(context):
    """
    Generating a reset token using uuid4 and adding a entry to
    database table, generate a reset link and send email address
    """
    resetcode = PasswordResetCode.objects.create(
        code=uuid4().hex,
        user_id=context['user_id']
    )
    context['password_reset_link'] = f'{settings.RESET_PASSWORD_URL}?code={resetcode.code}'

    mail_content = render_to_string(
        'accounts/emails/password_reset_link_mail.html',
        context
    )

    mail = EmailMessage(
        'Reset Password',
        mail_content,
        settings.EMAIL_FROM,
        to=[context['email_address']],
    )
    mail.content_subtype = "html"
    mail.send()
