from rest_framework import serializers

from tasks.models import Tasks
from tasks.serializers import TasksSerializer
from .models import CustomUser


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "email",
            "username",
            "phone_number",
            "city",
            "avatar",
        ]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    # tokens = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            "username",
            "email",
            "password",
        )

    def create(
        self, validated_data
    ):  # if we won't use create method password won't be saved using salt
        user = CustomUser.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user


class USerTasksSerializer(serializers.ModelSerializer):
    tasks = serializers.SerializerMethodField(read_only=True)
    number_of_active_tasks = serializers.IntegerField(read_only=True)
    class Meta:
        model = CustomUser
        fields = ('id','email','username','tasks', 'number_of_active_tasks')
        ordering = ['number_of_active_tasks']


    def get_tasks(self, user):
        qs = user.tasks.filter(status=Tasks.STARTED,)
        return TasksSerializer(qs, many=True).data


    # def get_number_of_active_tasks(self, instance):
    #     return (
    #         instance.tasks.filter(status=Tasks.STARTED).count()
    #     )
