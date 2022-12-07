from accounts import views
from django.urls import path

urlpatterns = [
    path(
        'register/',
        views.UserRegistrationAPIView.as_view(),
        name='user-register-api'
    ),
    path(
        'companies/',
        views.UserCompanyInfoAPIView.as_view(),
        name='user-company-info-complete-api'
    ),
]
