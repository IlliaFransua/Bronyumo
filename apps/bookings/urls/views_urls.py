from django.urls import path
from apps.bookings.views import ClientBookingPanelView

urlpatterns = [
    path('client-booking-panel/<str:entity_hash>/<str:map_image_hash>/',
         ClientBookingPanelView.as_view(),
         name='client-booking-panel-view'),
]
