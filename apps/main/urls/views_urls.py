from django.urls import path
from apps.main.views import HomePageView, EntrepreneurPageView

urlpatterns = [
    path('',
         HomePageView.as_view(),
         name='home-page-view'),

    path('entrepreneur/',
         EntrepreneurPageView.as_view(),
         name='entrepreneur-page-view'),
]
