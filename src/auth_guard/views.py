from rest_framework_simplejwt.views import TokenObtainPairView
from auth_guard.serializers import AuthLoginSerializer


class AuthLoginView(TokenObtainPairView):
    """
    Extending TokenObtainPairView of `Simple JWT` package.
    This view uses custom serializer which adds additional information to return
    once user is successfully authenticated.
    """
    serializer_class = AuthLoginSerializer
