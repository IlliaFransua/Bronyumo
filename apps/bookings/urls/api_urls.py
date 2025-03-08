from django.urls import path
from apps.bookings.api import CheckBookingAvailabilityAPI, CreateBookingAPI, UploadAndDeleteBookingsAPI, \
    UploadAndPreserveBookingsAPI, AddForBookingAPI, RemoveFromBookingAPI, ShareBookingAPI, DeleteBookingEntryAPI

urlpatterns = [
    path('check-booking-availability/<str:booking_hash>/',
         CheckBookingAvailabilityAPI.as_view(),
         name='check-booking-availability-api'),

    path('create-booking/<str:booking_hash>/',
         CreateBookingAPI.as_view(),
         name='create-booking-api'),

    path('upload-and-delete-bookings/<str:booking_hash>/',
         UploadAndDeleteBookingsAPI.as_view(),
         name='upload-and-delete-bookings-api'),

    path('upload-and-preserve-bookings/<str:booking_hash>/',
         UploadAndPreserveBookingsAPI.as_view(),
         name='upload-and-preserve-bookings-api'),
#
    path('add-for-booking/<str:booking_hash>/',
         AddForBookingAPI.as_view(),
         name='add-for-booking-api'),

    path('remove-from-booking/<str:booking_hash>/',
         RemoveFromBookingAPI.as_view(),
         name='remove-from-booking-api'),

    path('share-booking/<str:booking_hash>/',
         ShareBookingAPI.as_view(),
         name='share-booking-api'),

    path('check-booking-availability/<str:booking_hash>/',
         CheckBookingAvailabilityAPI.as_view(),
         name='check-booking-availability-api'),

    path('create-booking/<str:booking_hash>/',
         CreateBookingAPI.as_view(),
         name='create-booking-api'),

    path('delete-booking-entry/<str:booking_hash>/',
         DeleteBookingEntryAPI.as_view(),
         name='delete-booking-entry-api'),
]
