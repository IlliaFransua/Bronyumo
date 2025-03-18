from django.utils.decorators import method_decorator
from django.views import View
from typing import Optional
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from apps.utils.decorators import session_required
from rest_framework import status
from rest_framework.views import APIView
from apps.accounts.DatabaseConnection import DatabaseConnection
from apps.accounts.managers import CompanyManager, CompanySessionManager, MapManager
from Bronyumo.settings import db_dsn
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

# Example of model import
# from apps.main.models import yourModer


@method_decorator(session_required, name='dispatch')
class UploadAndPreserveBookingsAPI(APIView):
    def __init__(self, **kwargs: dict) -> None:
        super().__init__(**kwargs)
        self.db_dsn = db_dsn
        self.company_manager = CompanyManager(db_dsn=db_dsn)
        self.session_manager = CompanySessionManager(db_dsn=db_dsn)
        self.map_manager = MapManager(db_dsn=db_dsn)
    
    def post(self, request, map_hash)-> JsonResponse:
        image_path = self.map_manager.get_map_image_path(map_hash)
        if not image_path:
            return JsonResponse({"error": "Cannot find map_hash in DB."}, status=status.HTTP_400_BAD_REQUEST)
        image = request.FILES.get('floorPlanImage')
        if not image:
            return JsonResponse({"error": "No file provided."}, status=status.HTTP_400_BAD_REQUEST)
        default_storage.save(image_path, ContentFile(image.read()))
        return JsonResponse({'status': 'success'}, status=status.HTTP_200_OK)