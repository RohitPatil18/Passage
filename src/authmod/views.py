from rest_framework_simplejwt.views import TokenObtainPairView

from authmod.serializers import AuthLoginSerializer


class AuthLoginView(TokenObtainPairView):
    """
    Extending TokenObtainPairView of `Simple JWT` package.
    This view uses custom serializer which adds additional information to return
    once user is successfully authenticated.
    """

    serializer_class = AuthLoginSerializer
