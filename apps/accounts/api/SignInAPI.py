from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from apps.accounts.serializers import SignInSerializer


class SignInAPI(APIView):
    """
    Данный API-эндпоинт предназначен для обработки входа пользователя в систему.
    Использует стандартные методы валидации и проверки данных.

    Основные функции:
    - Прием POST-запроса с учетными данными.
    - Анализ и сверка переданных данных с базой данных.
    - В случае подтверждения учетной записи — генерация и передача токена доступа.
    - При несовпадении данных — формирование отчета об ошибке.

    Метод post работает в статическом режиме. Создание дополнительного экземпляра не требуется. Оптимальная эффективность обеспечена.
    """

    @staticmethod
    def post(request):
        """
        Параметры:
            request (Request): Входные данные пользователя.

        Ожидаемый формат данных:
            {
                "username": <строка>,
                "password": <строка>
            }

        Ожидаемый результат при успешном входе:
            {
                "token": <строка>,     # Сгенерированный токен доступа.
                "user_id": <число>,    # Уникальный идентификатор пользователя.
                "expires": <строка>    # Время окончания действия токена (формат ISO 8601).
            }

        В случае ошибки аутентификации:
            {
                "error": <строка>      # Причина отказа. Например, "Неверные учетные данные".
            }
        """
        serializer = SignInSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)

            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response(
                    {'message': 'Login has been completed successfully.', 'token': token.key},
                    status=status.HTTP_200_OK
                )
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
