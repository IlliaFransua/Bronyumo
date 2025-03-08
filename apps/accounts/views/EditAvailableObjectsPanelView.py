from django.views import View
from django.http import HttpResponse
from django.shortcuts import render

# Example of model import
# from apps.main.models import yourModer


class EditAvailableObjectsPanelView(View):
    @staticmethod
    def get(request, entity_hash, map_image_hash):
        """
        Handle GET requests.

        This method processes GET requests and returns an HTML page
        with a context containing a list of items.
        """
        context = {
            "items": ["one", "two", "three"],  # Example list of items
        }

        return render(request, "main/home.html", context)
