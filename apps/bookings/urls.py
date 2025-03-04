from django.urls import path
from .views import home, enrepreneur_page

urlpatterns = [
    path('', home, name='home'),
    path('test/', enrepreneur_page, name='enrepreneur_page'),
]
