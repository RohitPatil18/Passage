from django.urls import reverse
from faker import Faker
from rest_framework.test import APITestCase
from rest_framework import status

from accounts.models import UserTypeChoice

faker = Faker()


class UserRegisterAPITests(APITestCase):

    url = reverse('user-register-api')

    def test_user_register_success(self):
        """
        Test for successful API call
        """
        data = {
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "email_address": faker.free_email(),
            "user_type": UserTypeChoice.COMPANY_USER,
            "password": "R@ndrom#321",
            "confirm_password": "R@ndrom#321"
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['first_name'], data['first_name'])
        self.assertIsNone(response.data.get('password'))
        self.assertIsNone(response.data.get('confirm_password'))
