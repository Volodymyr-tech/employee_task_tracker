from django.db.models import Count, Q
from rest_framework import generics, viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated

from tasks.models import Tasks
from users.models import CustomUser
from users.serializers import RegisterSerializer, UserProfileSerializer, USerTasksSerializer


class RegisterView(CreateAPIView):
    """Registerview class, allow enyone to register"""

    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    # permission_classes = [AllowAny]  # allow anyone to register


class UserProfileViewSet(viewsets.ModelViewSet):
    """UserviewSet allows only authenticated users and admins to see and make changes in objects.
    Also, you can filter objects by username and email"""
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    # filter_backends = [SearchFilter, OrderingFilter]
    # search_fields = [
    #     "username",
    #     "email",
    # ]
    permission_classes = [IsAuthenticated, IsAdminUser]


    def get_permissions(self):
        """DRF requires all permissions to return True, and if at least one returns False, it will be 403"""
        if self.action in ["list", "retrieve"]:
            permission_classes = [
                IsAuthenticated,
            ]
        elif self.action in ["update", "partial_update"]:
            permission_classes = [
                IsAuthenticated,
                IsAdminUser,
            ]
        elif self.action == "create":
            permission_classes = [IsAuthenticated, IsAdminUser]
        elif self.action == "destroy":
            permission_classes = [
                IsAuthenticated,
                IsAdminUser,
            ]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]


class UserTasksApiView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.filter(tasks__status__exact='Started').distinct() # if do not use distinct we'll get duplicate
    serializer_class = USerTasksSerializer
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        return CustomUser.objects.annotate(
            number_of_active_tasks=Count('tasks', filter=Q(tasks__status=Tasks.STARTED))
        ).order_by('-number_of_active_tasks')
