import json

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.utils import timezone
from tasks.models import Tasks
from users.models import CustomUser

with open('./user.JSON', 'r', encoding='utf-8') as f:
    user_data = json.load(f)

with open('./users_list.JSON', 'r', encoding='utf-8') as f:
    users_list_data = json.load(f)


with open('tasks/fixtures/list_task_test.json', 'r', encoding='utf-8') as f:
    tasks_list_data = json.load(f)


with open('tasks/fixtures/task_test.json', 'r', encoding='utf-8') as f:
    task_test = json.load(f)
class SuggestedImportantTasksAPITest(APITestCase):
    def setUp(self):
        self.user_set = [CustomUser.objects.create_user(**user) for user in users_list_data]
        self.client.force_authenticate(user=self.user_set[0])
        self.tasks_set = [Tasks.objects.create(task=task.get('task'), performer=self.user_set[task.get('performer')],
                                               term=task.get('term'), status=task.get('status'),
                                               is_parent_task=task.get('is_parent_task')
                                               ) for task in tasks_list_data]

    def get_admine(self):
        admin = self.user_set[1]
        admin.is_staff = True
        return admin

    def test_api_returns_expected_task(self):
        url = f"http://127.0.0.1:8003/api/tasks/suggestions/"
        admin = self.get_admine()
        self.client.force_authenticate(user=admin)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)



class TasksViewSetAPITest(APITestCase):

    def setUp(self):
        self.user_set = [CustomUser.objects.create_user(**user) for user in users_list_data]
        self.client.force_authenticate(user=self.user_set[0])
        self.tasks_set = [Tasks.objects.create(task=task.get('task'), performer=self.user_set[task.get('performer')],
                                          term=task.get('term'), status=task.get('status'), is_parent_task=task.get('is_parent_task')
                                          ) for task in tasks_list_data]

    def get_admine(self):
        admin = self.user_set[1]
        admin.is_staff = True
        return admin


    def test_get_task(self):
        url = f"/api/tasks/{self.tasks_set[0].pk}/"
        response = self.client.get(url)
        dict_data = response.json()
        self.assertEqual(response.status_code, 200)


    def test_patch(self):
        url = f"/api/tasks/{self.tasks_set[0].pk}/"
        admin = self.get_admine()
        self.client.force_authenticate(user=admin)
        update_data = {
            "task": "Updated Task Title",
            "status": "Started"
        }

        response = self.client.patch(url, update_data, format="json")
        self.assertEqual(response.status_code, 200)

        data = response.json()

        for key, value in update_data.items():
            self.assertEqual(data[key], value)

    def test_create_task_denied(self):
        url = f"/api/tasks/"
        self.client.logout()
        response = self.client.post(url, task_test, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_delete_task_denied(self):
        url = f"/api/tasks/{self.tasks_set[0].pk}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_task(self):
        url = f"/api/tasks/{self.tasks_set[0].pk}/"
        admin = self.get_admine()
        self.client.force_authenticate(user=admin)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)