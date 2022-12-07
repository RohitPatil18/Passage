from rest_framework import generics

from accounts import serializers


class UserRegistrationAPIView(generics.CreateAPIView):
    """
    User registration API. This endpoint should be used to allow
    new registration.
    """
    serializer_class = serializers.UserCreateSerializer
    permission_classes = []
    authentication_classes = []


class UserCompanyInfoAPIView(generics.CreateAPIView):
    """
    After registration, we ask user to complete onboarding process where
    user is asked to fill out company information
    """
    serializer_class = serializers.CompanyUserSerializer
