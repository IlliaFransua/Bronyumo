from django.urls import path
from apps.accounts.views import EditAvailableObjectsPanelView, EntrepreneurPanelView, ReservationsPanelView

urlpatterns = [
    path('entrepreneur-panel/',
         EntrepreneurPanelView.as_view(),
         name='entrepreneur-panel-view'),

    path('edit-available-objects-panel/',
         EditAvailableObjectsPanelView.as_view(),
         name='edit-available-objects-panel-view'),

    path('reservations-panel/<str:entity_hash>/<str:map_image_hash>/',
         ReservationsPanelView.as_view(),
         name='reservations-panel-view'),
]
