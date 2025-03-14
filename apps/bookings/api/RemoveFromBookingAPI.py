from django.utils.decorators import method_decorator
from django.views import View
from django.http import HttpResponse
from django.shortcuts import render
from apps.utils.decorators import session_required


# Example of model import
# from apps.main.models import yourModer


@method_decorator(session_required, name='dispatch')
class RemoveFromBookingAPI(View):
    @staticmethod
    def get(request, map_hash, booking_object_hash):
        pass
