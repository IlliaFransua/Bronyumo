from django.views import View
from django.http import HttpResponse
from django.shortcuts import render

# Example of model import
# from apps.main.models import yourModel


# @method_decorator(session_required, name='dispatch')
class SaveMapAPI(View):
    @staticmethod
    def get(request, map_hash):
        pass
