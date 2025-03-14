from django.shortcuts import render
from django.views import View


# Example of model import
# from apps.main.models import yourModer


class EntrepreneurPageView(View):
    """
    Данный класс представляет собой обработчик HTTP-запросов для страницы предпринимателей.
    Использует метод GET для возврата целевой страницы.

    Основные функции:
    - Получение запроса от клиента.
    - Генерация HTML-ответа.
    - Возврат подготовленной страницы пользователю.

    Статический метод `get()` позволяет обработать запрос без создания экземпляра класса.
    """

    @staticmethod
    def get(request):
        """
        Ожидаемые параметры:
            request (HttpRequest): HTTP-запрос от клиента.

        Ожидаемый результат:
            HTTP-ответ с HTML-страницей.

        В этом примере возвращается заглушка с путем к HTML-шаблону.
        Если необходимо отобразить страницу, предпочтительно использовать `render()`.
        """
        return render(request, "main/EntrepreneurPageView.html")
