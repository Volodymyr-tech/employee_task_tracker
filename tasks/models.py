from django.db import models

from users.models import CustomUser


# Create your models here.



class Tasks(models.Model):

    CREATED = 'Created' #данные поля отображаются в БД
    STARTED = 'Started'
    DONE = 'Done'

    STATUS_CHOICES = [
        (CREATED, 'Created'), #данные поля отображаются в админке Django
        (STARTED, 'Started'),
        (DONE, 'Done'),
    ]

    task = models.CharField(max_length=255)
    performer = models.ForeignKey(
        CustomUser,
        null=True,
        blank=True,
        related_name="tasks",
        on_delete=models.SET_NULL,
    )
    parent_task = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL)
    term = models.DateTimeField()
    status = models.CharField(choices=STATUS_CHOICES)
    is_parent_task = models.BooleanField(null=True, blank=True)

