from django.urls import path

from apps.accounts.api import SignUpAPI, SignInAPI, LogoutAPI

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
]
