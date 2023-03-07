from datetime import timedelta

from django.conf import settings
from django.db import transaction
from django.utils import timezone
from rest_framework import serializers

from accounts.models import Company, PasswordResetCode, User, UserTypeChoice
from authmod.models import RoleChoice


class ConfirmPasswordInMixin(serializers.Serializer):
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        if validated_data.get("password") != validated_data.get("confirm_password"):
            raise serializers.ValidationError(
                {"password": "Password and Confirm Password do not match."}
            )
        validated_data.pop("confirm_password")
        return validated_data


class UserCreateSerializer(ConfirmPasswordInMixin, serializers.ModelSerializer):
    """
    Serializer for `User Registration` API
    """

    company_name = serializers.CharField(source="company.name")

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email_address",
            "company_name",
            "user_type",
            "password",
            "confirm_password",
        )
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate_user_type(self, value):
        """
        Only company users are allowed to register from this API
        """
        if value != UserTypeChoice.COMPANY_USER:
            raise serializers.ValidationError("Invalid user type.")
        return value

    @transaction.atomic
    def create(self, validated_data):
        company_data = validated_data.pop("company")
        company = Company.objects.create(name=company_data["name"])
        return User.objects.create(
            company=company,
            role_id=RoleChoice.COMPANY_ADMIN,
            **validated_data,
        )


class UserEmailInSerializer(serializers.Serializer):
    email_address = serializers.EmailField()


class PasswordResetInSerializer(ConfirmPasswordInMixin, serializers.Serializer):
    current_password = serializers.CharField()
    password = serializers.CharField()

    def validate_current_password(self, value):
        if not self.context["request"].user.check_password(value):
            raise serializers.ValidationError("Incorrect current password.")
        return value


class ResetCodeInSerializer(serializers.Serializer):
    code = serializers.CharField()

    def validate(self, attrs):
        validated_data = super().validate(attrs)

        # Validate Reset token and add
        limit = timezone.now() - timedelta(minutes=settings.RESET_PASSWORD_URL_EXPIRY)

        resetcode = PasswordResetCode.objects.filter(
            code=validated_data["code"], created_at__gt=limit
        ).first()

        if not resetcode:
            raise serializers.ValidationError("Password reset link is expired.")

        validated_data["resetcode"] = resetcode
        return validated_data


class ForgottenPasswordResetInSerializer(
    ConfirmPasswordInMixin,
    ResetCodeInSerializer,
):
    password = serializers.CharField()
