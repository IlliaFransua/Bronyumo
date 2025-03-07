from .BaseValidator import BaseValidator
from rest_framework import serializers

class PasswordStrengthValidator(BaseValidator):
    def validate(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must contain at least 8 characters.")
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError("Password must contain at least one digit.")
        return value
