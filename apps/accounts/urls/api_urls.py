from apps.accounts.api import SignUpAPI, SignInAPI, LogoutAPI, GetBookingObjectsAPI, GetMapImageAPI
from django.urls import path

urlpatterns = [
    path('sign-up/',
         SignUpAPI.as_view(),
         name='sign-up-api'),

    path('sign-in/',
         SignInAPI.as_view(),
         name='sign-in-api'),

    path('logout/',
         LogoutAPI.as_view(),
         name='logout-api'),

    path('get_map_image/<str:map_hash>/',
         GetMapImageAPI.as_view(),
         name='get-map-request-path-with-map-image'),

    path('get_booking_objects/<str:map_hash>/',
         GetBookingObjectsAPI.as_view(),
         name='get-map-request-path-with-booking-objects-api'),
]
