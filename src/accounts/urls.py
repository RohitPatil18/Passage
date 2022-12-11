from accounts import views
from django.urls import path

urlpatterns = [
    path(
        'register',
        views.UserRegistrationAPIView.as_view(),
        name='user-register-api'
    ),
    path(
        'companies',
        views.UserCompanyInfoAPIView.as_view(),
        name='user-company-info-complete-api'
    ),
    path(
        'password/forgot/initiate',
        views.ForgotPasswordInitiateAPIView.as_view(),
        name='user-forgot-password-initiate-api'
    ),
    path(
        'password/forgot/verify',
        views.ForgotPasswordCodeVerifyAPIView.as_view(),
        name='user-forgot-password-code-verify-api'
    ),
    path(
        'password/forgot/reset',
        views.ForgotPasswordResetAPIView.as_view(),
        name='user-forgot-password-reset-api'
    ),
    path(
        'password/reset',
        views.PasswordResetAPIView.as_view(),
        name='user-password-reset-api'
    ),
]
