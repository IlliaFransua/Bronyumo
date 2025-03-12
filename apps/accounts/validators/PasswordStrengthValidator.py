from .BaseValidator import BaseValidator
from rest_framework import serializers


class PasswordStrengthValidator(BaseValidator):
    """
    Данный валидатор оценивает сложность пароля на основе длины и наличия цифр.
    В случае несоответствия минимальным требованиям пароль отвергается.
    """

    def validate(self, value):
        """
        Проверка надежности пароля.

        Требования к паролю:
        - Минимальная длина — 8 символов.
        - Максимальная длина — 64 символа.
        - Должен содержать хотя бы одну цифру (0-9).
        - Должен содержать хотя бы одну заглавную букву (A-Z).
        - Должен содержать хотя бы одну строчную букву (a-z).
        - Должен содержать хотя бы один специальный символ (!@#$%^&*()-_=+[]{}|;:'",.<>?/).

        Если пароль не соответствует требованиям, процесс регистрации останавливается.
        """
        if len(value) < 8:
            raise serializers.ValidationError("Пароль должен содержать не менее 8 символов.")
        if len(value) > 64:
            raise serializers.ValidationError("Пароль пароль слишком длинный")
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError("Пароль должен содержать хотя бы одну цифру.")
        if not any(char.islower() for char in value):
            raise serializers.ValidationError("Пароль должен содержать хотя бы одну строчную букву.")
        if not any(char.isupper() for char in value):
            raise serializers.ValidationError("Пароль должен содержать хотя бы одну прописную букву.")
        if not any(char in "!@#$%^&*()-_=+[]{}|;:,.<>?/" for char in value):
            raise serializers.ValidationError("Пароль должен содержать хотя бы один специальный символ.")

        return value
