from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from authmod.views import AuthLoginView

urlpatterns = [
    path("login", AuthLoginView.as_view(), name="auth_login_api"),
    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
]
