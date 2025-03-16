from typing import Optional

from Bronyumo.settings import db_dsn
from apps.accounts.managers import CompanyManager, CompanySessionManager
from apps.accounts.managers import MapManager
from apps.utils.decorators import session_required
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework import status


@method_decorator(session_required, name='dispatch')
class DeleteBookingObjectAPI(View):
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

    def delete(self, request, map_hash: str, booking_object_hash: str):
        """
        Удаляет объект бронирования для указанной карты по хешу объекта.

        :param map_hash: Хеш карты из пути.
        :param booking_object_hash: Хеш объекта бронирования для удаления.
        :return: JSON с сообщением об успехе или ошибке.
        """
        try:
            session_id = request.COOKIES.get('session_id')
            company_data: Optional[dict] = self.company_manager.get_company_by_session_id(session_id)
            if not company_data:
                return JsonResponse({"error": "Company not found."}, status=status.HTTP_400_BAD_REQUEST)

            company_id = company_data.get("id")

            if not self.map_manager.map_belongs_to_company(map_hash, company_id):
                return JsonResponse({"error": "Карта не принадлежит компании."}, status=status.HTTP_403_FORBIDDEN)

            if not self.map_manager.delete_booking_object(map_hash, booking_object_hash):
                return JsonResponse({"error": "Объект бронирования не найден."}, status=status.HTTP_404_NOT_FOUND)

            return JsonResponse({"message": "Объект бронирования успешно удален."}, status=status.HTTP_200_OK)

        except Exception as e:
            return JsonResponse({"error": "Произошла ошибка: " + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
