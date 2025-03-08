from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.accounts.serializers import SignUpSerializer


class SignUpAPI(APIView):
    """
    Этот API-эндпоинт предназначен для создания новой учетной записи пользователя.
    Использует алгоритмы валидации и проверки данных для обеспечения корректного процесса регистрации.

    Основные функции:
    - Прием POST-запроса с регистрационными данными.
    - Проверка уникальности учетной записи.
    - Хеширование пароля перед сохранением.
    - Создание новой записи в базе данных.
    - Возврат подтверждения успешной регистрации или ошибки.

    Метод post работает в статическом режиме. Создание дополнительного экземпляра не требуется. Оптимальная эффективность обеспечена.
    """

    @staticmethod
    def post(request):
        """
        Параметры:
            request (Request): Данные пользователя, переданные для регистрации.

        Ожидаемый формат данных:
            {
                "username": <строка>,
                "password": <строка>,
                "email": <строка>
            }

        Ожидаемый результат при успешной регистрации:
            {
                "user_id": <число>,    # Уникальный идентификатор нового пользователя.
                "message": "Registration has been completed successfully."
            }

        В случае ошибки регистрации:
            {
                "error": <строка>      # Причина отказа, например "Имя пользователя уже занято".
            }
        """
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {'message': 'Registration has been completed successfully.', 'username': user.username},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
