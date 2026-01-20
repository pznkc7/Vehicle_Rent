from django.urls import path
from . import views
urlpatterns = [
    path('book/<int:vehicle_id>/', views.create_booking, name='create_booking'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('my/', views.my_bookings, name='my_bookings'),
    path('confirm-pickup/<int:booking_id>/', views.confirm_pickup, name='confirm_pickup'),
    path('owner/', views.owner_bookings, name='owner_bookings'),

    

]