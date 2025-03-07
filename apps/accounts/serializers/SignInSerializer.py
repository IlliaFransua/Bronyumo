from django.contrib.auth import authenticate
from rest_framework import serializers
from apps.accounts.validators import PasswordStrengthValidator


class SignInSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    @staticmethod
    def validate_password(self, value):
        """
        Validation of the password for compliance with security requirements.
        """
        validator = PasswordStrengthValidator()
        return validator.validate(value)

    def validate(self, data):
        """
        Checking username and password, user authentication.
        """
        username = data.get("username")
        password = data.get("password")

        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError("Invalid username or password")

        data["user"] = user  # Pass user to validated_data
        return data
