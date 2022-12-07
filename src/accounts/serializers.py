from rest_framework import serializers

from accounts import services
from accounts.models import Company, CompanyUser, User, UserTypeChoice


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for `User Registration` API
    """

    confirm_password = serializers.CharField(write_only=True)

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

    def validate(self, validated_data):
        if validated_data.get('password') != validated_data.get('confirm_password'):
            raise serializers.ValidationError({
                'password': 'Password and Confirm Password do not match.'
            })
        validated_data.pop("confirm_password")
        return validated_data


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
