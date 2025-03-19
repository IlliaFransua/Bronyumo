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
        try:
            super().__init__(**kwargs)
            self.company_manager = CompanyManager(db_dsn=db_dsn)
            self.session_manager = CompanySessionManager(db_dsn=db_dsn)
            self.map_manager = MapManager(db_dsn=db_dsn)
        except Exception as e:
            raise e

    def post(self, request, map_hash: str):
        try:
            data = json.loads(request.body)
            print("Получаемые данные на обнову:", data.get("booking_objects"))
            booking_availability = data.get("booking_availability")

            for booking_object in data.get("booking_objects", []):
                booking_object["booking_availability"] = booking_availability

            response = self.check_map_belongs_to_company(request, map_hash)
            if response:
                return response

            booking_object_hashes = []
            for booking_object in data.get("booking_objects", []):
                response = self.validate_booking_object(booking_object)
                if response:
                    return response

                availability_data = self.transform_availability_data(booking_object.get("booking_availability"))

                updated_hashes = self.map_manager.update_booking_objects(
                    map_hash,
                    data.get("booking_objects", [])
                )
                booking_object_hashes = updated_hashes

            return JsonResponse({"message": "Reservation objects successfully saved or updated.",
                                 "booking_object_hashes": booking_object_hashes}, status=status.HTTP_200_OK)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def check_map_belongs_to_company(self, request, map_hash: str) -> Optional[JsonResponse]:
        session_id = request.COOKIES.get('session_id')
        company_data = self.company_manager.get_company_by_session_id(session_id)
        if not company_data:
            return JsonResponse({"error": "Company not found."}, status=status.HTTP_400_BAD_REQUEST)

        company_id = company_data.get("id")
        if not self.map_manager.map_belongs_to_company(map_hash, company_id):
            return JsonResponse({"error": "The map does not belong to the company."}, status=status.HTTP_403_FORBIDDEN)

        return None

    def validate_booking_object(self, booking_object: dict) -> Optional[JsonResponse]:
        required_fields = ["x_min", "x_max", "y_min", "y_max", "booking_availability"]
        if not all(field in booking_object for field in required_fields):
            return JsonResponse({"error": "All parameters for booking objects must be passed."},
                                status=status.HTTP_400_BAD_REQUEST)
        return None

    def transform_availability_data(self, booking_availability: dict) -> dict:
        availability_data = {}
        for day, times in booking_availability.items():
            availability_data[day] = [{"open": time["open"], "close": time["close"]} for time in times]
        return availability_data
