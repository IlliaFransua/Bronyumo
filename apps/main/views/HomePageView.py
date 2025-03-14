from django.views import View
from django.http import HttpResponse
from django.shortcuts import render

# Example of model import
# from apps.main.models import yourModer


class HomePageView(View):
    """
    Этот класс отвечает за обработку HTTP-запросов к главной странице приложения.
    Использует метод GET для передачи данных и рендеринга HTML-шаблона.

    Основные функции:
    - Получение GET-запроса от клиента.
    - Подготовка контекста с данными.
    - Отображение HTML-шаблона с переданными параметрами.

    Статический метод `get()` позволяет обработать запрос без создания экземпляра класса.
    """

    @staticmethod
    def get(request):
        """
        Ожидаемые параметры:
            request (HttpRequest): Входящий HTTP-запрос.

        Ожидаемый результат:
            HTML-страница с переданными данными.

        В текущей версии передается список элементов в качестве примера.
        Если необходимо отобразить страницу, предпочтительно использовать `render()`.
        """

        return render(request, "main/HomePageView.html")
