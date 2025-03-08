from .BaseValidator import BaseValidator
from django.contrib.auth.models import User
from rest_framework import serializers


class UniqueUsernameValidator(BaseValidator):
    """
    Этот валидатор анализирует базу данных, чтобы убедиться, что имя пользователя
    не используется другим пользователем.
    """

    def validate(self, value):
        """
        Проверка имени пользователя. Запрос в базу данных.

        - Если имя уже зарегистрировано, регистрация останавливается.
        - В случае уникальности процесс продолжается.

        Дублирование учетных записей не допускается.
        """
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Пользователь с таким именем уже существует.")
        return value