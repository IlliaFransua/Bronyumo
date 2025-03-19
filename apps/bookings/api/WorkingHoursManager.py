from typing import Optional
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.views import APIView

from Bronyumo.settings import db_dsn
from apps.accounts.managers import CompanyManager, CompanySessionManager, MapManager
from apps.utils.decorators import session_required


@method_decorator(session_required, name='dispatch')
class WorkingHoursManager(APIView):
    def __init__(self, **kwargs):
        try:
            super().__init__(**kwargs)
            self.company_manager = CompanyManager(db_dsn=db_dsn)
            self.session_manager = CompanySessionManager(db_dsn=db_dsn)
            self.map_manager = MapManager(db_dsn=db_dsn)
        except Exception as e:
            raise e

    def get(self, request, map_hash: str, object_hash: Optional[str] = None):
        try:
            if not object_hash:
                booking_objects = self.map_manager.get_booking_objects_by_map_hash(map_hash)
                if not booking_objects:
                    return JsonResponse({"error": "No booking objects found for this map."},
                                        status=status.HTTP_404_NOT_FOUND)
                object_hash = booking_objects[0]['booking_object_hash']

            response = self.check_belongings(request, map_hash, object_hash)
            if response:
                return response

            booking_objects = self.map_manager.get_booking_objects_by_map_hash(map_hash)
            if not booking_objects:
                return JsonResponse({"error": "Booking object not found."}, status=status.HTTP_404_NOT_FOUND)

            return JsonResponse(booking_objects[0], status=status.HTTP_200_OK)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, map_hash: str, object_hash: str = None):
        try:
            if object_hash:
                response = self.check_belongings(request, map_hash, object_hash)
                if response:
                    print(f"Access check failed for object_hash: {object_hash}")
                    return response

            try:
                data = request.data
                booking_availability = data.get('booking_availability')
                if not booking_availability:
                    print("Error: Booking availability is required.")
                    return JsonResponse({"error": "Booking availability is required."},
                                        status=status.HTTP_400_BAD_REQUEST)

                if object_hash:
                    print(f"Updating booking hours for object_hash: {object_hash}")
                    update_result = self.map_manager.update_booking_object_hours(object_hash, booking_availability)
                else:
                    print(f"Updating booking hours for all objects on map_hash: {map_hash}")
                    update_result = self.map_manager.update_all_booking_objects_hours(map_hash, booking_availability)

                if not update_result:
                    print("Error: Failed to update booking hours.")
                    return JsonResponse({"error": "Failed to update booking hours."},
                                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                print(f"Executing query with map_hash: {map_hash} and availability: {booking_availability}")

                print(update_result)
                print("Booking hours updated successfully.")
                return JsonResponse({"message": "Booking hours updated successfully."}, status=status.HTTP_200_OK)

            except Exception as e:
                print(f"Error: Invalid JSON data: {str(e)}")
                return JsonResponse({"error": f"Invalid JSON data: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(f"Error processing request: {str(e)}")
            return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def check_map_belongs_to_company(self, request, map_hash: str) -> Optional[JsonResponse]:
        session_id = request.COOKIES.get('session_id')
        company_data = self.company_manager.get_company_by_session_id(session_id)
        if not company_data:
            return JsonResponse({"error": "Company not found."}, status=400)

        company_id = company_data.get("id")
        if not self.map_manager.map_belongs_to_company(map_hash, company_id):
            return JsonResponse({"error": "The map does not belong to the company."}, status=403)

        return None

    def check_booking_object_belongs_to_map(self, map_hash: str, object_hash: str) -> Optional[JsonResponse]:
        if not self.map_manager.check_booking_object_belongs_to_map(map_hash, object_hash):
            return JsonResponse({"error": "The booking object does not belong to this card."}, status=403)
        return None

    def check_belongings(self, request, map_hash: str, object_hash: str):
        response = self.check_map_belongs_to_company(request, map_hash)
        if response:
            return response

        response = self.check_booking_object_belongs_to_map(map_hash, object_hash)
        if response:
            return response

        return None
