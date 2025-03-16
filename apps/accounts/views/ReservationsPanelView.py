from django.views import View
from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework import status
from django.shortcuts import render
from accounts.managers import BookingManager, MapManager
from Bronyumo.settings import db_dsn

# Example of model import
# from apps.main.models import yourModer


class ReservationsPanelView(View):
    def get(self,request, map_hash):
        """
        Handle GET requests.

        This method processes GET requests and returns an HTML page
        with a context containing a list of items.
        """
        bookingManager = BookingManager(db_dsn)
        mapManager = MapManager(db_dsn)
        if not mapManager.check_map_hash_existence(map_hash):
            return JsonResponse({"error": "map doesn't exist"}, status=status.HTTP_404_NOT_FOUND)
        bookings = bookingManager.get_list_of_bookings_by_hash(map_hash)
        return render(request, "accounts/ReservationsPanelView.html", {'bookings': bookings})
