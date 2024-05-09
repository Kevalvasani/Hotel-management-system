from django.urls import path
from booking.views.booking_views import *
urlpatterns = [
    path('booking/<int:pk>',HotelBookingView.as_view(), name='booking'),
    path("booking/list/", HotelBookingShowView.as_view(), name="show_bookings"),
    path("bookings/list/", AllBookingtoAdminView.as_view(), name="admin_all_bookings"),
    path("bookings/cancel/<int:pk>/", CancelBookingsView.as_view(), name="cancel_bookings"),
]
    