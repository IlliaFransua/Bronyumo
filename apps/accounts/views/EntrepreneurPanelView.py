from typing import Optional

from django.core.exceptions import ObjectDoesNotExist
from django.http.response import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from Bronyumo.settings import db_dsn
from apps.accounts.managers import CompanyManager, MapManager, CompanySessionManager
from apps.utils.decorators import session_required


# Example of model import
# from apps.main.models import yourModer


@method_decorator(session_required, name='dispatch')
class EntrepreneurPanelView(View):
    """
    Данный класс обрабатывает HTTP-запросы, связанные со стартовой
    панелью управления предпринимателя, когда карта ещё не загружена.
    Использует метод GET для рендеринга HTML-шаблона с переданными параметрами.

    Основные функции:
    - Получение GET-запроса от клиента.
    - Формирование контекста с данными.
    - Генерация HTML-ответа с подготовленной информацией.

    Метод `get()` работает в статическом режиме. Создание экземпляра класса не требуется.
    """

    def __init__(self, **kwargs: Optional[dict]) -> None:
        """
        Initializes the view. Sets up the company and session managers for use.

        :param kwargs: Additional keyword arguments passed to the parent class.
        """
        try:
            super().__init__(**kwargs)
            self.company_manager = CompanyManager(db_dsn=db_dsn)
            self.session_manager = CompanySessionManager(db_dsn=db_dsn)
            self.map_manager = MapManager(db_dsn=db_dsn)
        except Exception as e:
            # print(f"Error during initialization: {str(e)}")
            raise

    def get(self, request, status=None):
        """
        Ожидаемые параметры:
            request (HttpRequest): HTTP-запрос, полученный от клиента.

        Ожидаемый результат:
            HTML-страница, содержащая переданный контекст.

        В текущей версии передается список элементов в качестве примера.
        Если необходимо отобразить страницу, предпочтительно использовать `render()`.
        """
        try:
            session_id: Optional[str] = request.COOKIES.get('session_id')

            company_data: Optional[dict] = self.company_manager.get_company_by_session_id(session_id)

            return render(request, "accounts/EntrepreneurPanelView.html", {"company_name": company_data.get("name")})

        except ObjectDoesNotExist as e:
            return JsonResponse({"error": "Company data not found."}, status=status.HTTP_404_NOT_FOUND)
        except KeyError as e:
            return JsonResponse({"error": f"Missing key: {str(e)}."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return JsonResponse({"error": "An unexpected error occurred."},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
