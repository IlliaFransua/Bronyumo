from rest_framework.views import APIView
from rest_framework.response import Response

# Example of model import
# from apps.main.models import yourModer


class CreateBookingAPI(APIView):
    @staticmethod
    def get(request, booking_hash):
        # Create booking logic
        availability_data = {
            "available": True,
            "message": "Booking is created.",
            "booking_hash": booking_hash,
        }

        return Response(availability_data)

