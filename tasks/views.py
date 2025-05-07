from django.db.models import Count, Min, Q
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from tasks.models import Tasks
from tasks.serializers import TasksSerializer, SuggestedTaskSerializer
from users.models import CustomUser
from users.paginators import StandardResultsSetPagination
from users.permissions import IsUser


# Create your views here.

class TasksViewSet(viewsets.ModelViewSet):
    """UserviewSet allows only authenticated users and admins to see and make changes in objects.
    Also you can filter objects by username and email"""

    queryset = Tasks.objects.all()
    serializer_class = TasksSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = [
        "is_public",
        "action",
    ]
    permission_classes = [IsAuthenticated, IsUser]
    pagination_class = StandardResultsSetPagination

    def get_permissions(self):
        """DRF requires all permissions to return True, and if at least one returns False, it will be 403"""
        if self.action in ["list", "retrieve"]:
            permission_classes = [
                IsAuthenticated
            ]  # authenticated users can view
        elif self.action in ["update", "partial_update"]:
            permission_classes = [
                IsAuthenticated,
                IsUser
            ]  # only admins and owners can change tasks
        elif self.action == "create":
            permission_classes = [IsAuthenticated]  # anyone can create tasks
        elif self.action == "destroy":
            permission_classes = [
                IsAuthenticated, IsAdminUser
            ]  # only admins can delete tasks
        else:
            # Добавляем значение по умолчанию, если self.action не соответствует ни одному из вышеуказанных вариантов
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    #
    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)


class SuggestedImportantTasksAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        important_tasks = Tasks.objects.filter(
            status=Tasks.CREATED,
            is_parent_task=False,
            parent_task__isnull=False,
            parent_task__status=Tasks.STARTED
        )

        users_qs = CustomUser.objects.annotate(
            active_task_count=Count('tasks', filter=Q(tasks__status=Tasks.STARTED))
        )

        # 3. Минимальная загрузка
        min_count = users_qs.aggregate(
            Min("active_task_count")
        )["active_task_count__min"] or 0

        available_users = users_qs.filter(active_task_count__lte=min_count + 2)

        result = []

        for task in important_tasks:
            suggested_users = []

            parent_user = task.parent_task.performer if task.parent_task else None

            if parent_user and available_users.filter(id=parent_user.id).exists():
                suggested_users.append(parent_user.username)
            elif available_users.exists():
                least_loaded = available_users.order_by("active_task_count").first()
                suggested_users.append(least_loaded.username)

            result.append({
                "task": task.task,
                "deadline": task.term,
                "suggested_employees": suggested_users
            })

        serializer = SuggestedTaskSerializer(result, many=True)
        return Response(serializer.data)