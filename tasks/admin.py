from django.contrib import admin

from tasks.models import Tasks


# Register your models here.
@admin.register(Tasks)
class TasksAdmin(admin.ModelAdmin):
    list_display = (
        "task",
        "performer",
        "status",
    )