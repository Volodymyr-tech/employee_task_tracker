# Generated by Django 5.2 on 2025-05-06 19:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_tasks_is_parent_task'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='tasks',
            name='performer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tasks', to=settings.AUTH_USER_MODEL),
        ),
    ]
