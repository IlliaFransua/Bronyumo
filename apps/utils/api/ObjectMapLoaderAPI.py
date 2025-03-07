from django.views import View
from django.http import HttpResponse
from django.shortcuts import render

# Example of model import
# from apps.main.models import yourModer


class ObjectMapLoaderAPI(View):
    @staticmethod
    def get(request, entity_hash, map_image_hash, *args, **kwargs):
        pass
