from django.utils.decorators import method_decorator
from django.views import View
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from Bronyumo.settings import db_dsn
from apps.accounts.managers import MapManager
from apps.utils.decorators import session_required
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from datetime import datetime


@method_decorator(session_required, name='dispatch')
class ObjectsMapLoaderAPI(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.map_manager = MapManager(db_dsn=db_dsn)

    def get(self, request, map_hash):
        try:
            from_time = request.query_params.get('from')
            to_time = request.query_params.get('to')

            if not from_time or not to_time:
                return Response({"error": "Missing 'from' or 'to' parameters."}, status=status.HTTP_400_BAD_REQUEST)

            # Использование strptime для обработки строк в формате ISO 8601 (с учетом UTC)
            from_time = datetime.strptime(from_time, "%Y-%m-%dT%H:%M:%S.%fZ")
            to_time = datetime.strptime(to_time, "%Y-%m-%dT%H:%M:%S.%fZ")

            available_objects = self.map_manager.get_available_booking_objects(map_hash, from_time, to_time)
            return Response({"booking_objects": available_objects}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
