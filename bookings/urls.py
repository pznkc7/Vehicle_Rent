from django.urls import path
from . import views
urlpatterns = [
    path('book/<int:vehicle_id>/', views.create_booking, name='create_booking'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('my/', views.my_bookings, name='my_bookings'),
    path('owner/', views.owner_bookings, name='owner_bookings'),
    path(
        'owner/booking/<int:booking_id>/accept/',
        views.owner_accept_booking,
        name='owner_accept_booking'
    ),
    path(
        'owner/booking/<int:booking_id>/reject/',
        views.owner_reject_booking,
        name='owner_reject_booking'
    ),
     # -------------------- PICKUP CONFIRMATION --------------
    path(
        'confirm-pickup/<int:booking_id>/',
        views.confirm_pickup,
        name='confirm_pickup'
    ),

    # -------------------- RETURN CONFIRMATION --------------
    path(
        'confirm-return/<int:booking_id>/',
        views.confirm_return,
        name='confirm_return'
    ),

    

]