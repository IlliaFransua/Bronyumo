from django.views import View
from django.http import HttpResponse
from django.shortcuts import render

# Example of model import
# from apps.main.models import yourModel


class SaveMapAPI(View):
    @staticmethod
    def get(request, booking_hash):
        pass
