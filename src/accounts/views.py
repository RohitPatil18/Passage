from django.http import HttpResponse
from rest_framework import generics
from rest_framework.exceptions import ValidationError

from accounts import serializers
from accounts.models import User
from accounts.services import reset_user_password
from core.mixins import PublicAPIMixin
from core.views import PostServiceAPIView
from notifications.events import USER_PASSWORD_RESET_LINK
from notifications.tasks import notify_user


class UserRegistrationAPIView(PublicAPIMixin, generics.CreateAPIView):
    """
    User registration API. This endpoint should be used to allow
    new registration.
    """

    serializer_class = serializers.UserCreateSerializer


class PasswordResetAPIView(PostServiceAPIView):
    """
    This API allows logged in user to reset account password
    """

    serializer_class = serializers.PasswordResetInSerializer

    def process_request(self, request, serializer):
        return reset_user_password(
            request, request.user, serializer.validated_data["password"]
        )


class ForgotPasswordInitiateAPIView(PublicAPIMixin, PostServiceAPIView):
    """
    API to initiate request to reset password when user was unable to login.
    Sends mail along with reset link to user if email exists
    """

    serializer_class = serializers.UserEmailInSerializer
    response_message = "Please check you email for password reset link."

    def process_request(self, _, serializer):
        try:
            user = User.objects.get(
                email_address=serializer.validated_data["email_address"]
            )
        except User.DoesNotExist:
            raise ValidationError(
                code="invalid_email_address",
                detail="User with given email address not found.",
            )

        notify_user(
            USER_PASSWORD_RESET_LINK,
            recepients=user,
            context={"user_id": user.id, "email_address": user.email_address},
        )
        return user


class ForgotPasswordCodeVerifyAPIView(PublicAPIMixin, PostServiceAPIView):
    """
    This API checks if Reset Code exists in database and created before expiry time
    """

    serializer_class = serializers.ResetCodeInSerializer
    response_message = "Password reset link is valid."


class ForgotPasswordResetAPIView(PublicAPIMixin, PostServiceAPIView):
    """
    This API accepts reset code and password and changes user's password
    """

    serializer_class = serializers.ForgottenPasswordResetInSerializer
    response_message = "Password successfully changed."

    def process_request(self, request, serializer):
        resetcode = serializer.validated_data["resetcode"]
        reset_user_password(
            request, resetcode.user, serializer.validated_data["password"]
        )
        resetcode.delete()

