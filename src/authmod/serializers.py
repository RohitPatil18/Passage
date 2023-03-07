from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'email_address',
            'user_type'
        )


class AuthLoginSerializer(TokenObtainPairSerializer):
    """
    Extends `TokenObtainPairSerializer` serializer from `SimpleJWT` package.
    AReturns additional user information in response body
    """

    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = UserSerializer(self.user).data
        return data
