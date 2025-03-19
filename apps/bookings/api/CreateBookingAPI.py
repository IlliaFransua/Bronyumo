from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from Bronyumo.settings import db_dsn
from apps.accounts.managers import MapManager


# Example of model import
# from apps.main.models import yourModer


class CreateBookingAPI(APIView):
    def __init__(self, **kwargs):
        try:
            super().__init__(**kwargs)
            self.map_manager = MapManager(db_dsn=db_dsn)
        except Exception as e:
            raise e

    def post(self, request, map_hash, booking_objects_hash):
        booking_data = request.data

        first_name = booking_data.get('first_name')
        last_name = booking_data.get('last_name')
        email = booking_data.get('email')
        phone = booking_data.get('phone')
        booking_period = {"from": "2025-03-20T10:00:00", "to": "2025-03-20T12:00:00"}  # Пример периода

        if not first_name or not last_name or not email or not phone:
            return Response({"error": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            if not self.map_manager.check_booking_object_belongs_to_map(map_hash, booking_objects_hash):
                return Response({"error": "Booking object does not belong to the map."},
                                status=status.HTTP_400_BAD_REQUEST)

            # Сохраняем запись бронирования
            self.map_manager.save_booking_record(booking_objects_hash, first_name, last_name, email, phone,
                                                 booking_period)

            return Response({"message": "Booking created successfully."}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
