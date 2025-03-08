from django.contrib.auth import authenticate
from rest_framework import serializers
from apps.accounts.validators import PasswordStrengthValidator


class SignInSerializer(serializers.Serializer):
    """
    Данный сериализатор выполняет проверку имени пользователя и пароля,
    гарантируя соответствие требованиям безопасности перед авторизацией.

    Ожидаемый входной JSON:
        {
            "username": <строка>,   # Имя пользователя
            "password": <строка>    # Пароль пользователя
        }

    Ожидаемый выходной JSON при успешной аутентификации:
        {
            "user_id": <число>,     # Уникальный идентификатор пользователя
            "username": <строка>,   # Имя пользователя
            "token": <строка>,      # Токен доступа (например, JWT)
            "message": "Аутентификация успешна."
        }

    Ожидаемый выходной JSON при ошибке аутентификации:
        {
            "error": <строка>       # Описание ошибки, например "Неверные учетные данные."
        }
    """

    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    @staticmethod
    def validate_password(value):
        """
        Проверка пароля на соответствие установленным стандартам безопасности.

        Используется встроенный валидатор. В случае несоответствия дальнейшая обработка невозможна.
        """
        validator = PasswordStrengthValidator()
        return validator.validate(value)

    def validate(self, data):
        """
        Верификация учетных данных. Идентификация пользователя в системе.

        Операция выполняется в два этапа:
        1. Извлечение имени пользователя и пароля из входных данных.
        2. Аутентификация пользователя на основе полученной информации.

        Если учетные данные некорректны, процесс завершается с ошибкой.
        В случае успеха идентифицированный пользователь передается в `validated_data` для дальнейшего использования.
        """
        username = data.get("username")
        password = data.get("password")

        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError({"error": "Неверные учетные данные."})

        # Генерация токена (можно использовать JWT или другой механизм)
        token = "generated_token_example"

        return {
            "user_id": user.id,
            "username": user.username,
            "token": token,
            "message": "Аутентификация успешна."
        }
