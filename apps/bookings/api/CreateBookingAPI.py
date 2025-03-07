from rest_framework.views import APIView
from rest_framework.response import Response

# Example of model import
# from apps.main.models import yourModer


class CreateBookingAPI(APIView):
    @staticmethod
    def get(self, request, entity_hash, map_image_hash, *args, **kwargs):
        # Create booking logic
        availability_data = {
            "available": True,
            "message": "Booking is created.",
            "entity_hash": entity_hash,
            "map_image_hash": map_image_hash
        }

        return Response(availability_data)

