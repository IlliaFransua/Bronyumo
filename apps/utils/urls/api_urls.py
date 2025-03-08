from django.urls import path
from apps.utils.api import MapUploadAPI, ObjectMapLoaderAPI, SaveMapAPI

urlpatterns = [
    path('map-upload/',
         MapUploadAPI.as_view(),
         name='map-upload-api'),

    path('object-map-loader/<str:booking_hash>/',
         ObjectMapLoaderAPI.as_view(),
         name='object-map-loader-api'),

    path('save-map/<str:booking_hash>/',
         SaveMapAPI.as_view(),
         name='save-map-api'),
]
