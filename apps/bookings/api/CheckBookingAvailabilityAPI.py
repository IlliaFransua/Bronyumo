from rest_framework.views import APIView
from rest_framework.response import Response

# Example of model import
# from apps.main.models import yourModer


class CheckBookingAvailabilityAPI(APIView):
    @staticmethod
    def get(request, map_hash):
        # Check booking availability logic
        availability_data = {
            "available": True,
            "message": "Booking is available.",
            "map_hash": map_hash,
        }

        return Response(availability_data)
