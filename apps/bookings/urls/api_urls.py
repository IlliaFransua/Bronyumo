from apps.bookings.api import CheckBookingAvailabilityAPI, CreateBookingAPI, UploadAndDeleteBookingsAPI, \
    UploadAndPreserveBookingsAPI, AddForBookingAPI, RemoveFromBookingAPI, ShareBookingAPI, DeleteBookingEntryAPI, \
    DeleteBookingObjectAPI, SaveBookingObjectsAPI
from django.urls import path

urlpatterns = [
    path('check-booking-availability/<str:map_hash>/',
         CheckBookingAvailabilityAPI.as_view(),
         name='check-booking-availability-api'),

    path('create-booking/<str:map_hash>/',
         CreateBookingAPI.as_view(),
         name='create-booking-api'),

    path('upload-and-delete-bookings/<str:map_hash>/',
         UploadAndDeleteBookingsAPI.as_view(),
         name='upload-and-delete-bookings-api'),

    path('upload-and-preserve-bookings/<str:map_hash>/',
         UploadAndPreserveBookingsAPI.as_view(),
         name='upload-and-preserve-bookings-api'),

    path('add-for-booking/<str:map_hash>/',
         AddForBookingAPI.as_view(),
         name='add-for-booking-api'),

    path('save-booking-objects/<str:map_hash>/',
         SaveBookingObjectsAPI.as_view(),
         name='save-booking-objects'),

    path('delete-booking-object/<str:map_hash>/<str:booking_object_hash>/',
         DeleteBookingObjectAPI.as_view(),
         name='delete-booking-object'),

    path('remove-from-booking/<str:map_hash>/<str:booking_object_hash>/',
         RemoveFromBookingAPI.as_view(),
         name='remove-from-booking-api'),

    path('share-booking/<str:map_hash>/',
         ShareBookingAPI.as_view(),
         name='share-booking-api'),

    path('check-booking-availability/<str:map_hash>/',
         CheckBookingAvailabilityAPI.as_view(),
         name='check-booking-availability-api'),

    path('create-booking/<str:map_hash>/',
         CreateBookingAPI.as_view(),
         name='create-booking-api'),

    path('delete-booking-entry/<str:map_hash>/',
         DeleteBookingEntryAPI.as_view(),
         name='delete-booking-entry-api'),
]
