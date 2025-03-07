from django.contrib.auth.models import User
from rest_framework import serializers
from apps.accounts.validators import PasswordStrengthValidator, UniqueUsernameValidator


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    username = serializers.CharField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    @staticmethod
    def validate_password(value):
        validator = PasswordStrengthValidator()
        return validator.validate(value)

    @staticmethod
    def validate_username(self, value):
        validator = UniqueUsernameValidator()
        return validator.validate(value)

    def create(self, validated_data):
        # We use create_user user for correct password hashing
        user = User.objects.create_user(**validated_data)
        return user