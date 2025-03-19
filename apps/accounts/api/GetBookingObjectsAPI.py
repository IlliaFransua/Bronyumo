from typing import Optional

from Bronyumo.settings import db_dsn
from apps.accounts.managers import CompanyManager, CompanySessionManager, MapManager
from apps.utils.decorators import session_required
from django.http.request import HttpRequest
from django.http.response import JsonResponse
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


@method_decorator(session_required, name='dispatch')
class GetBookingObjectsAPI(APIView):
    """
    API endpoint for retrieving a map's booking objects and its image.

    Verifies that the provided map_hash belongs to the company associated with the current session.
    Then, it returns a JSON containing:
      - map_hash: The provided map identifier.
      - image_url: The absolute URL of the map image.
      - booking_objects: A list of booking objects with their coordinates and booking availability.
    """

    def __init__(self, **kwargs: Optional[dict]) -> None:
        """
        Initializes the API endpoint with the necessary managers.

        Parameters:
            kwargs (Optional[dict]): Additional keyword arguments.
        """
        try:
            super().__init__(**kwargs)
            self.company_manager = CompanyManager(db_dsn=db_dsn)
            self.session_manager = CompanySessionManager(db_dsn=db_dsn)
            self.map_manager = MapManager(db_dsn=db_dsn)
        except Exception as e:
            raise e

    def get(self, request: HttpRequest, map_hash: str) -> JsonResponse:
        """
        Handles GET requests to retrieve booking objects and the map image URL for a given map hash.

        Parameters:
            request (HttpRequest): The HTTP request object with session cookies.
            map_hash (str): The unique identifier of the map.

        Returns:
            Response: A JSON response containing:
                - "map_hash" (str): The provided map hash.
                - "image_url" (str): The absolute URL of the map image.
                - "booking_objects" (list): A list of booking objects with coordinates and booking availability.
            If the map does not belong to the company, or if an error occurs, an appropriate error message is returned.
        """
        try:
            session_id: Optional[str] = request.COOKIES.get('session_id')
            company_data: Optional[dict] = self.company_manager.get_company_by_session_id(session_id)
            if not company_data:
                return JsonResponse({"error": "Company not found."}, status=status.HTTP_400_BAD_REQUEST)

            company_id = company_data.get("id")
            if not self.map_manager.map_belongs_to_company(map_hash, company_id):
                return JsonResponse({"error": "Map does not belong to the company."}, status=status.HTTP_403_FORBIDDEN)

            booking_objects = self.map_manager.get_booking_objects_by_map_hash(map_hash)

            response_data = {
                "map_hash": map_hash,
                "booking_objects": booking_objects
            }
            print(JsonResponse(response_data, status=status.HTTP_200_OK))
            return JsonResponse(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return JsonResponse({"error": "An unexpected error occurred: " + str(e)},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
