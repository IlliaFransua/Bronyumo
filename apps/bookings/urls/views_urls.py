from django.urls import path
from apps.bookings.views import ClientBookingPanelView

urlpatterns = [
    path('client-booking-panel/<str:booking_hash>/',
         ClientBookingPanelView.as_view(),
         name='client-booking-panel-view'),
]
