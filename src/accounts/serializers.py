from datetime import timedelta

from django.conf import settings
from django.utils import timezone
from rest_framework import serializers

from accounts import services
from accounts.models import (Company, CompanyUser, PasswordResetCode, User,
                             UserTypeChoice)


class ConfirmPasswordInMixin(serializers.Serializer):
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        if validated_data.get('password') != validated_data.get('confirm_password'):
            raise serializers.ValidationError({
                'password': 'Password and Confirm Password do not match.'
            })
        validated_data.pop("confirm_password")
        return validated_data


class UserCreateSerializer(ConfirmPasswordInMixin, serializers.ModelSerializer):
    """
    Serializer for `User Registration` API
    """
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email_address',
            'user_type',
            'password',
            'confirm_password'
        )
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate_user_type(self, value):
        """
        Only company users are allowed to register from this API
        """
        if value != UserTypeChoice.COMPANY_USER:
            raise serializers.ValidationError(
                'Invalid user type.'
            )
        return value


class CompanyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = (
            'name',
        )

    def validate(self, validated_data):
        user = self.context['request'].user
        if user.user_type != UserTypeChoice.COMPANY_USER:
            raise serializers.ValidationError(
                {
                    'error': 'Invalid user type.'
                }
            )
        if CompanyUser.objects.filter(user=user).exists():
            raise serializers.ValidationError(
                {
                    'error': 'Company information is already added for user.'
                }
            )
        return validated_data

    def create(self, validated_data):
        """
        DRF's default function is overridden and control is passed to service
        layer for further processing of data
        """
        return services.add_user_company_information(
            self.context['request'].user,
            validated_data
        )


class UserEmailInSerializer(serializers.Serializer):
    email_address = serializers.EmailField()


class PasswordResetInSerializer(ConfirmPasswordInMixin, serializers.Serializer):
    current_password = serializers.CharField()
    password = serializers.CharField()

    def validate_current_password(self, value):
        if not self.context['request'].user.check_password(value):
            raise serializers.ValidationError('Incorrect current password.')
        return value


class ResetCodeInSerializer(serializers.Serializer):
    code = serializers.CharField()

    def validate(self, attrs):
        validated_data = super().validate(attrs)

        # Validate Reset token and add
        limit = timezone.now() - timedelta(minutes=settings.RESET_PASSWORD_URL_EXPIRY)

        resetcode = PasswordResetCode.objects \
            .filter(code=validated_data['code'], created_at__gt=limit)\
            .first()

        if not resetcode:
            raise serializers.ValidationError(
                'Password reset link is expired.'
            )

        validated_data['resetcode'] = resetcode
        return validated_data


class ForgottenPasswordResetInSerializer(
    ConfirmPasswordInMixin,
    ResetCodeInSerializer,
):
    password = serializers.CharField()
