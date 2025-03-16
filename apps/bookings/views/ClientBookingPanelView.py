from django.http import HttpResponse
from django.views import View


# Example of model import
# from apps.main.models import yourModer


class ClientBookingPanelView(View):
    @staticmethod
    def get(request, map_hash):
        """
        Handle GET requests.

        This method processes GET requests and returns an HTML page.
        """
        return HttpResponse(f"Map Hash: {map_hash}")
