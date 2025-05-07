import json

from rest_framework import status
from rest_framework.status import HTTP_403_FORBIDDEN
from rest_framework.test import APITestCase, APITransactionTestCase
from users.models import CustomUser
# Create your tests here.
with open('./user.JSON', 'r', encoding='utf-8') as f:
    user_data = json.load(f)

with open('./users_list.JSON', 'r', encoding='utf-8') as f:
    users_list_data = json.load(f)

class UsersViewSetTestCase(APITestCase):

    def setUp(self):
        self.user_set = [CustomUser.objects.create_user(**user) for user in users_list_data]
        self.client.force_authenticate(user=self.user_set[0])

    def get_admine(self):
        admin = self.user_set[1]
        admin.is_staff = True
        return admin


    def test_get_user(self):
        url = f"/api/users/profiles/{self.user_set[0].pk}/"
        response = self.client.get(url)
        dict_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(dict_data.get("email"), "ivan.petrov@example.com")


    def test_get_users_list(self):
        url = f"/api/users/profiles/"
        response = self.client.get(url)
        dict_data = response.json()
        raw = json.dumps(dict_data)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(raw, users_list_data)

    def test_patch(self):
        url = f"/api/users/profiles/{self.user_set[0].pk}/"
        admin = self.get_admine()
        self.client.force_authenticate(user=admin)
        response = self.client.patch(url, user_data, format="json")
        dict_data = response.json()
        raw = json.dumps(dict_data)
        self.assertJSONEqual(raw, user_data)



    def test_create_user_denied(self):
        url = f"/api/users/profiles/"
        response = self.client.post(url, user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)



    def test_delete_user_denied(self):
        url = f"/api/users/profiles/{self.user_set[2].pk}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

