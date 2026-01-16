from django.urls import path
from . import views
urlpatterns = [
    path('book/<int:vehicle_id>/', views.create_booking, name='create_booking'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    
    

]