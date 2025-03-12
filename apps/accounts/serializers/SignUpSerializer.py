from django.contrib.auth import get_user_model
from rest_framework import serializers
from apps.accounts.validators import PasswordStrengthValidator

User = get_user_model()


class SignUpSerializer(serializers.Serializer):
    """
    Данный сериализатор выполняет обработку регистрационной информации,
    проверяя корректность введенных данных и создавая нового пользователя в системе.

    Ожидаемый входной JSON:
        {
            "username": <строка>,   # Уникальное имя пользователя
            "password": <строка>,   # Надежный пароль, соответствующий требованиям безопасности
            "email": <строка>       # Действительный email-адрес
        }

    Ожидаемый выходной JSON при успешной регистрации:
        {
            "user_id": <число>,     # Уникальный идентификатор нового пользователя
            "username": <строка>,   # Имя пользователя
            "email": <строка>,      # Email пользователя
            "message": "Регистрация успешно завершена."
        }

    Ожидаемый выходной JSON при ошибке регистрации:
        {
            "error": <строка>       # Описание ошибки, например "Имя пользователя уже занято."
        }
    """

    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField()

    @staticmethod
    def validate_password(value):
        """
        Проверка пароля на соответствие стандартам безопасности.

        Используется встроенный валидатор, обеспечивающий контроль сложности пароля.
        В случае несоответствия регистрация будет отклонена.
        """
        validator = PasswordStrengthValidator()
        return validator.validate(value)

    @staticmethod
    def validate_username(value):
        """
        Проверка уникальности имени пользователя.

        Если имя уже используется, регистрация невозможна.
        """
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Имя пользователя уже занято.")
        return value

    @staticmethod
    def validate_email(value):
        """
        Проверка уникальности email-адреса.

        Если email уже зарегистрирован, система предотвращает создание дубликата.
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Этот email уже используется.")
        return value

    def create(self, validated_data):
        """
        Создание нового пользователя в системе.

        Операция выполняется с учетом предварительно проверенных данных.
        Пароль сохраняется в зашифрованном виде.
        """
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"]
        )
        return user

