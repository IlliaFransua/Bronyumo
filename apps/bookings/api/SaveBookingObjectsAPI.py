import json
from typing import Optional

from Bronyumo.settings import db_dsn
from apps.accounts.managers import CompanyManager, CompanySessionManager, MapManager
from apps.utils.decorators import session_required
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.views import APIView


@method_decorator(session_required, name='dispatch')
class SaveBookingObjectsAPI(APIView):
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
        Сохраняет или обновляет объекты бронирования, привязанные к указанной карте.

        :param map_hash: Хеш карты.
        :return: JSON с результатом операции.
        """
        try:
            data = json.loads(request.body)
            booking_availability = data.get("booking_availability")

            for booking_object in data.get("booking_objects", []):
                booking_object["booking_availability"] = booking_availability

            print("Преобразованные данные:", json.dumps(data, indent=2))

            print("Полученный map_hash:", map_hash)

            session_id = request.COOKIES.get('session_id')
            company_data: Optional[dict] = self.company_manager.get_company_by_session_id(session_id)
            if not company_data:
                return JsonResponse({"error": "Компания не найдена."}, status=status.HTTP_400_BAD_REQUEST)

            company_id = company_data.get("id")

            if not self.map_manager.map_belongs_to_company(map_hash, company_id):
                return JsonResponse({"error": "Карта не принадлежит компании."}, status=status.HTTP_403_FORBIDDEN)

            booking_object_hashes = []
            for booking_object in data.get("booking_objects", []):
                x_min = booking_object.get("x_min")
                x_max = booking_object.get("x_max")
                y_min = booking_object.get("y_min")
                y_max = booking_object.get("y_max")
                booking_availability = booking_object.get("booking_availability")

                if not all([x_min, x_max, y_min, y_max, booking_availability]):
                    return JsonResponse({"error": "Все параметры для объектов бронирования должны быть переданы."},
                                        status=status.HTTP_400_BAD_REQUEST)

                availability_data = {}
                for day, times in booking_availability.items():
                    availability_data[day] = [{"open": time["open"], "close": time["close"]} for time in times]

                booking_object_hash = self.map_manager.save_or_update_booking_object(
                    map_hash, x_min, x_max, y_min, y_max, availability_data)
                booking_object_hashes.append(booking_object_hash)

            return JsonResponse({"message": "Объекты бронирования успешно сохранены или обновлены.",
                                 "booking_object_hashes": booking_object_hashes}, status=status.HTTP_200_OK)

        except Exception as e:
            return JsonResponse({"error": "Произошла ошибка: " + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
