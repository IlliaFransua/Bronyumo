from django.views import View
from django.http import HttpResponse
from django.shortcuts import render

# Example of model import
# from apps.main.models import yourModer


class ClientBookingPanelView(View):
    @staticmethod
    def get(self, request, entity_hash, card_hash):
        """
        Handle GET requests.

        This method processes GET requests and returns an HTML page.
        """
        return HttpResponse(f"Entity Hash: {entity_hash}, Card Hash: {card_hash}")
