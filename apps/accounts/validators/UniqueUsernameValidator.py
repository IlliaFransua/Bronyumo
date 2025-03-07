from .BaseValidator import BaseValidator
from django.contrib.auth.models import User
from rest_framework import serializers

class UniqueUsernameValidator(BaseValidator):
    def validate(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("User with this name already exists.")
        return value
