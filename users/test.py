from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class AuthTests(APITestCase):

    def test_register_user_success(self):
        url = r"http://127.0.0.1:8003/api/users/register/"
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "StrongPass123",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="testuser").exists())