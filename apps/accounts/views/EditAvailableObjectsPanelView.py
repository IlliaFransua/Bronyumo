import json
from typing import Optional

from Bronyumo.settings import db_dsn
from apps.accounts.managers import CompanyManager, CompanySessionManager, MapManager
from apps.utils.decorators import session_required
from django.http import JsonResponse
from django.http.request import HttpRequest
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework import status


@method_decorator(session_required, name='dispatch')
class EditAvailableObjectsPanelView(View):
    def __init__(self, **kwargs: Optional[dict]) -> None:
        """
        Initializes the view. Sets up the company and session managers for use.

        :param kwargs: Additional keyword arguments passed to the parent class.
        """
        try:
            super().__init__(**kwargs)
            self.company_manager = CompanyManager(db_dsn=db_dsn)
            self.session_manager = CompanySessionManager(db_dsn=db_dsn)
            self.map_manager = MapManager(db_dsn=db_dsn)
        except Exception as e:
            # print(f"Error during initialization: {str(e)}")
            raise

    def get(self, request: HttpRequest, map_hash: str) -> JsonResponse:
        """
        Handles GET requests to return booking data for a given map hash after verifying that the map belongs to the company.

        Parameters:
            request (HttpRequest): The HTTP request object, including the session cookie.
            map_hash (str): The unique identifier of the map.

        Returns:
            JsonResponse: A JSON object containing:
                - "map_hash" (str): The provided map hash.
                - "booking_availability" (dict): The booking availability data (by days of the week).
                - "booking_objects" (list): A list of booking objects with coordinates.
            If the map does not belong to the company or if any error occurs, an appropriate error message is returned.
        """
        try:
            session_id: str = request.COOKIES.get('session_id')
            company_data: Optional[dict, None] = self.company_manager.get_company_by_session_id(session_id)
            if not company_data:
                return JsonResponse({"error": "Company not found."}, status=status.HTTP_400_BAD_REQUEST)

            company_id = company_data.get("id")

            if not self.map_manager.map_belongs_to_company(map_hash, company_id):
                return JsonResponse({"error": "Map does not belong to the company."}, status=status.HTTP_403_FORBIDDEN)

            booking_objects = self.map_manager.get_booking_objects_by_map_hash(map_hash)
            print(booking_objects)

            return render(request, "accounts/EditAvailableObjectsPanelView.html", {
                "company_name": company_data.get("name"),
                "booking_objects": json.dumps(booking_objects),
            })

        except Exception as e:
            return JsonResponse({"error": f"An unexpected error occurred: {str(e)}"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
