from rest_framework import serializers

from tasks.models import Tasks
from tasks.validators import ConnectedTaskOrIsParentValidator


class TasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = "__all__"
        validators = [ConnectedTaskOrIsParentValidator('is_parent_task', 'parent_task')]

class SuggestedTaskSerializer(serializers.Serializer):
    task = serializers.CharField()
    deadline = serializers.DateTimeField()
    suggested_employees = serializers.ListField(child=serializers.CharField())

