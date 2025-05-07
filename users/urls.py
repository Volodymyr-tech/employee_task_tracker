from django.urls import include, path
from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    RegisterView,
    UserProfileViewSet, UserTasksApiView,
)

router = DefaultRouter()
router.register(r"profiles", UserProfileViewSet)  # Register the ViewSet is necessary

app_name = "users"

urlpatterns = [
    path("", include(router.urls)),
    path("tasks/", UserTasksApiView.as_view(), name="user_tasks"),
    path("register/", RegisterView.as_view(), name="register"),
    path(
        "login/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="token_obtain_pair",
    ),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
