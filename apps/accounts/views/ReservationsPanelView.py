from django.views import View
from django.http import HttpResponse
from django.shortcuts import render

# Example of model import
# from apps.main.models import yourModer


class ReservationsPanelView(View):
    @staticmethod
    def get(request, *args, **kwargs):
        """
        Handle GET requests.

        This method processes GET requests and returns an HTML page
        with a context containing a list of items.
        """
        context = {
            "items": ["one", "two", "three"],  # Example list of items
        }

        return render(request, "main/home.html", context)
