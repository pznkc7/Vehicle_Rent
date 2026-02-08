from django.urls import path
from . import views
urlpatterns = [
    path('book/<int:vehicle_id>/', views.create_booking,name='create_booking'),
    path('notifications/inbox/', views.notification_inbox, name='notification_inbox'),
    path('notifications/read/<int:notification_id>/', views.mark_notification_read, name='mark_notification_read'),
    path('notifications/read-all/', views.mark_all_notifications_read, name='mark_all_notifications_read'),
    path('my-bookings/', views.my_bookings,name='my_bookings'),
    path('incoming-bookings/', views.owner_bookings,name='owner_bookings'),
    path('owner/booking/<int:booking_id>/accept/',views.owner_accept_booking,name='owner_accept_booking'),
    path('owner/booking/<int:booking_id>/reject/',views.owner_reject_booking,name='owner_reject_booking'),
    path('confirm-pickup/<int:booking_id>/',views.confirm_pickup,name='confirm_pickup'),
    path('confirm-return/<int:booking_id>/',views.confirm_return,name='confirm_return'),    
        


    

]