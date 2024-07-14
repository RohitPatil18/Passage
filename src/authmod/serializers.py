from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from accounts.serializers import UserInfoSerializer


class AuthLoginSerializer(TokenObtainPairSerializer):
    """
    Extends `TokenObtainPairSerializer` serializer from `SimpleJWT` package.
    AReturns additional user information in response body
    """

    def validate(self, attrs):
        data = super().validate(attrs)
        data["user"] = UserInfoSerializer(self.user).data
        return data
