from rest_framework import serializers


class BaseValidator:
    def __init__(self, *args):
        """When creating a validator object,
        we can pass any number of fields"""
        self.fields = args

    def __call__(self, value):
        print(f" here are {self.fields}")
        field_values = {
            field: value.get(field) for field in self.fields
        }  # getting the dict of values from serializer, can be string,int, objects etc.
        print(field_values)
        self.validate(
            **field_values
        )  # pass dict with values to validation func

    def validate(self, **kwargs):
        """Abstract method"""
        raise NotImplementedError(
            "You should realize that method in your validation classes"
        )


class ConnectedTaskOrIsParentValidator(BaseValidator):
    """
    Checks that the associated habit and reward are not specified at the same time.
    """

    def validate(self, is_parent_task, parent_task, **kwargs):
        if is_parent_task and parent_task:
            raise serializers.ValidationError(
                "Simultaneous selection of a parent status and"
                " related task is prohibited"
            )

