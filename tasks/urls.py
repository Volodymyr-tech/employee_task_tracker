from django.urls import include, path
from rest_framework.routers import DefaultRouter

from tasks.views import TasksViewSet, SuggestedImportantTasksAPIView

router = DefaultRouter()
router.register(r"tasks", TasksViewSet)


app_name = "tasks"

urlpatterns = [
    path("tasks/suggestions/", SuggestedImportantTasksAPIView.as_view(), name="important_tasks"),# if root begins from router PREFIX it wont be find
    path("", include(router.urls)),  # Include the generated API endpoints

]
