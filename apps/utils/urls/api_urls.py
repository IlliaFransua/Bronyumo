from django.urls import path
from apps.utils.api import MapUploadAPI, ObjectsMapLoaderAPI, SaveMapAPI

urlpatterns = [
    path('map-upload/',
         MapUploadAPI.as_view(),
         name='map-upload-api'),

    path('objects-map-loader/<str:map_hash>/',
         ObjectsMapLoaderAPI.as_view(),
         name='object-map-loader-api'),

    path('save-map/<str:map_hash>/',
         SaveMapAPI.as_view(),
         name='save-map-api'),
]
