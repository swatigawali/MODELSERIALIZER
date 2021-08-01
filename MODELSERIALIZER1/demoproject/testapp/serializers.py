from rest_framework import serializers
from .models import Task

class Taskserializer(serializers.ModelSerializer):
    class Meta:
        model=Task
        fields= "__all__"

    def validate_title(self,value):# automatically call when serializer.save() get call in put method
        print('Validate at field level')
        if value != value.upper():
            raise serializers.ValidationError('Title should be in capital')
        return value
