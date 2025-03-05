from django.urls import path
from .views import home, enrepreneur_page, save_table_layout

urlpatterns = [
    path('', home, name='home'),
    path('entrepreneur-panel/', enrepreneur_page, name='enrepreneur_page'),
    path('save-table-layout/', save_table_layout, name="save_table_layout")
]
