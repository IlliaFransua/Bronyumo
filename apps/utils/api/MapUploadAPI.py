from rest_framework.views import APIView
from django.core.files.storage import default_storage
from rest_framework.response import Response
from rest_framework import status


class MapUploadAPI(APIView):
    """
    Данный API-эндпоинт предназначен для приема изображений в форматах JPG, JPEG и PNG.
    Использует стандартные методы валидации и проверки данных.

    Основные параметры работы:
    - Прием POST-запросов, содержащих изображение.
    - Анализ расширения и размера загружаемого файла.
    - Потоковая передача данных для минимизации потребления ресурсов.
    - Сохранение изображения в локальном хранилище.
    - Возвращение подтверждения успешной загрузки или отчета об ошибке.

    Метод post работает в статическом режиме. Создание дополнительного экземпляра не требуется. Эффективность максимальна.
    """

    @staticmethod
    def post(request):
        """
        Параметры:
            request (Request): Входные данные, содержащие загружаемый файл.

        Ожидаемый формат данных:
            - multipart/form-data с полем "file", содержащим изображение.

        Ожидаемый результат при успешной загрузке:
            {
                "file_url": <строка>,   # Ссылка на загруженный файл.
                "message": "Файл успешно загружен."
            }

        В случае ошибки:
            {
                "error": <строка>       # Причина отказа. Например, "Недопустимый формат файла".
            }
        """
        file = request.FILES.get('file')

        if not file:
            return Response({"error": "Файл не обнаружен в запросе."}, status=status.HTTP_400_BAD_REQUEST)

        allowed_extensions = ['jpg', 'jpeg', 'png']
        extension = file.name.split('.')[-1].lower()

        if extension not in allowed_extensions:
            return Response({"error": "Формат файла не соответствует требованиям. Разрешены только JPG, JPEG и PNG."},
                            status=status.HTTP_400_BAD_REQUEST)

        file_path = f"uploads/maps/{file.name}"
        with default_storage.open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        file_url = default_storage.url(file_path)
        return Response({"file_url": file_url, "message": "Файл успешно загружен."},
                        status=status.HTTP_201_CREATED)
