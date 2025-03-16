from apps.bookings.views import ClientBookingPanelView
from django.urls import path

urlpatterns = [
    path('client-booking-panel/<str:map_hash>/',
         ClientBookingPanelView.as_view(),
         name='client-booking-panel-view'),
]
