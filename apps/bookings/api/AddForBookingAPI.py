import json
from typing import Optional

from Bronyumo.settings import db_dsn
from apps.accounts.managers import CompanyManager, CompanySessionManager
from apps.accounts.managers import MapManager
from apps.utils.decorators import session_required
from django.core.exceptions import BadRequest
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework import status


@method_decorator(session_required, name='dispatch')
class AddForBookingAPI(View):
    def __init__(self, **kwargs):
        """
        Инициализирует API с необходимыми менеджерами.
        """
        try:
            super().__init__(**kwargs)
            self.company_manager = CompanyManager(db_dsn=db_dsn)
            self.session_manager = CompanySessionManager(db_dsn=db_dsn)
            self.map_manager = MapManager(db_dsn=db_dsn)
        except Exception as e:
            raise e

    def post(self, request, map_hash: str):
        """
        Создает новый объект бронирования для указанной карты с координатами и доступностью.
        Сначала проверяется, принадлежит ли карта компании, затем создается объект бронирования.

        :param map_hash: Хеш карты из пути.
        :return: JSON с хешем объекта или ошибкой.
        """
        try:
            session_id = request.COOKIES.get('session_id')
            company_data: Optional[dict] = self.company_manager.get_company_by_session_id(session_id)
            if not company_data:
                return JsonResponse({"error": "Company not found."}, status=status.HTTP_400_BAD_REQUEST)

            company_id = company_data.get("id")

            if not self.map_manager.map_belongs_to_company(map_hash, company_id):
                return JsonResponse({"error": "Карта не принадлежит компании."}, status=status.HTTP_403_FORBIDDEN)

            data = json.loads(request.body.decode('utf-8'))

            x_min = data.get('x_min')
            x_max = data.get('x_max')
            y_min = data.get('y_min')
            y_max = data.get('y_max')
            booking_availability = data.get('booking_availability')

            if None in [x_min, x_max, y_min, y_max, booking_availability]:
                raise BadRequest("Отсутствуют обязательные параметры.")

            booking_object_hash = self.map_manager.create_booking_object(
                map_hash, x_min, x_max, y_min, y_max, booking_availability
            )

            return JsonResponse({"booking_object_hash": booking_object_hash}, status=status.HTTP_201_CREATED)

        except BadRequest as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return JsonResponse({"error": "Произошла ошибка: " + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
