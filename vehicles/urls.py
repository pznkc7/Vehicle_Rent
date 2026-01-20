from django.urls import path
from . import  views 

urlpatterns = [
    path('vehicles/', views.vehicles, name='vehicles'),
    path('vehicles/<int:vehicle_id>/', views.vehicle_detail, name='vehicle_detail'),
    path('vehicles/apply_vehicle/', views.apply_vehicle, name='apply_vehicle'),
    path('my-applications/', views.my_vehicle_applications, name='my_vehicle_applications'),
    path('vehicles/apply/success/', views.vehicle_application_success, name='vehicle_application_success'),
    path('my-vehicles/', views.my_vehicles, name='my_vehicles'),
]
