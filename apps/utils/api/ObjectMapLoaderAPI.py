from django.views import View
from django.http import HttpResponse
from django.shortcuts import render

# Example of model import
# from apps.main.models import yourModer


# @method_decorator(session_required, name='dispatch')
class ObjectMapLoaderAPI(View):
    @staticmethod
    def get(request, map_hash):
        pass
