from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from tasks.models import Tasks
from tasks.serializers import TasksSerializer
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


class ListImportantTaskAPIView(ListAPIView):
    queryset = Tasks.objects.all()
    serializer_class = TasksSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination


    def get_queryset(self):
        return Tasks.objects.filter(status='Started', is_parent_task=True)