from datetime import timedelta

from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from accounts import models
from authmod.models import RoleChoice

faker = Faker()


def create_test_company():
    return models.Company.objects.create(name=faker.company())


def create_test_user():
    company = create_test_company()
    data = {
        "first_name": faker.first_name(),
        "last_name": faker.last_name(),
        "email_address": faker.free_email(),
        "user_type": models.UserTypeChoice.COMPANY_USER,
        "role_id": RoleChoice.COMPANY_ADMIN,
        "company": company,
        "password": faker.password(),
    }
    return models.User.objects.create(**data)


class UserRegisterAPITests(APITestCase):
    url = reverse("user-register-api")

    def test_user_register_success(self):
        """
        Test for successful API call
        """
        data = {
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "email_address": faker.free_email(),
            "user_type": models.UserTypeChoice.COMPANY_USER,
            "company_name": faker.company(),
            "password": "R@ndrom#321",
            "confirm_password": "R@ndrom#321",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["first_name"], data["first_name"])
        self.assertIsNone(response.data.get("password"))
        self.assertIsNone(response.data.get("confirm_password"))


class UserPasswordResetAPITests(APITestCase):
    """
    Test cases to test password reset flow.
    """

    def test_forgot_password_init(self):
        user = create_test_user()

        url = reverse("user-forgot-password-initiate-api")

        response = self.client.post(
            url,
            {"email_address": user.email_address},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_forgot_password_verify_200(self):
        """
        This case succeed when password token is available in database
        """
        user = create_test_user()
        codeobj = models.PasswordResetCode.objects.create(
            user=user, code="somerandomtokenindatabase"
        )

        url = reverse("user-forgot-password-code-verify-api")

        response = self.client.post(
            url,
            {"code": codeobj.code},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_forgot_password_verify_400(self):
        """
        This case succeed when password token is not available in database
        """

        url = reverse("user-forgot-password-code-verify-api")

        response = self.client.post(
            url,
            {"code": "somerandomtokennotindatabase"},
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_forgot_password_reset_success(self):
        """
        Reset password success use case
        """
        user = create_test_user()
        codeobj = models.PasswordResetCode.objects.create(
            user=user, code="passwordresetsuccesscode"
        )

        url = reverse("user-forgot-password-reset-api")

        payload = {
            "code": codeobj.code,
            "password": "notSoRandomPass@11",
            "confirm_password": "notSoRandomPass@11",
        }

        response = self.client.post(url, payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        codeobj = models.PasswordResetCode.objects.filter(id=codeobj.id)
        self.assertFalse(codeobj.exists())  # Checks if code is deleted from DB

        user.refresh_from_db()
        self.assertTrue(
            user.check_password(payload["password"])
        )  # checks password change

    def test_forgot_password_reset_failure(self):
        """
        Reset password failure: token expired
        """
        user = create_test_user()
        codeobj1 = models.PasswordResetCode.objects.create(
            user=user,
            code="expiredpasswordcode",
        )
        codeobj1.created_at = timezone.now() - timedelta(
            minutes=settings.RESET_PASSWORD_URL_EXPIRY
        )
        codeobj1.save()

        url = reverse("user-forgot-password-reset-api")

        payload = {
            "code": codeobj1.code,
            "password": "notSoRandomPass@11",
            "confirm_password": "notSoRandomPass@11",
        }

        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
