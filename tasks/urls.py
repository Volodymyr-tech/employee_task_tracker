from django.urls import include, path
from rest_framework.routers import DefaultRouter

from tasks.views import TasksViewSet, ListImportantTaskAPIView

router = DefaultRouter()
router.register(r"tasks", TasksViewSet)


app_name = "tasks"

urlpatterns = [
    path("tasks/important/", ListImportantTaskAPIView.as_view(), name="important_tasks"),# if root begins from router PREFIX it wont be find
    path("", include(router.urls)),  # Include the generated API endpoints

]
