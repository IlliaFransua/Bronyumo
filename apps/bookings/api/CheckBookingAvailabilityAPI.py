from rest_framework.views import APIView
from rest_framework.response import Response

# Example of model import
# from apps.main.models import yourModer


class CheckBookingAvailabilityAPI(APIView):
    @staticmethod
    def get(request, entity_hash, map_image_hash, *args, **kwargs):
        # Check booking availability logic
        availability_data = {
            "available": True,
            "message": "Booking is available.",
            "entity_hash": entity_hash,
            "map_image_hash": map_image_hash
        }

        return Response(availability_data)
