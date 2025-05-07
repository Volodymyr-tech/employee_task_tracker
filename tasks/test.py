from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.utils import timezone
from tasks.models import Tasks
from users.models import CustomUser


class SuggestedImportantTasksAPITest(APITestCase):
    def setUp(self):

        self.user1 = CustomUser.objects.create_user(email='user1@example.com', password='pass', username='u1')
        self.user2 = CustomUser.objects.create_user(email='user2@example.com', password='pass', username='u2')

        self.client.login(email='user1@example.com', password='pass')


        self.parent_task = Tasks.objects.create(
            task='Parent Task',
            status=Tasks.CREATED,
            is_parent_task=True,
            performer=None,
            term=timezone.now() + timezone.timedelta(days=3)
        )


        self.child_task = Tasks.objects.create(
            task='Child Task',
            status=Tasks.STARTED,
            parent_task=self.parent_task,
            performer=self.user2,
            term=timezone.now() + timezone.timedelta(days=2)
        )

    def test_api_returns_expected_task(self):
        url = f"http://127.0.0.1:8003/api/tasks/suggestions/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        task_data = response.data[0]
        self.assertEqual(task_data["task"], "Parent Task")
        self.assertIn("deadline", task_data)
        self.assertIn("suggested_employees", task_data)
        self.assertIsInstance(task_data["suggested_employees"], list)
