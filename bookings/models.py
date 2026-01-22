# bookings/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from vehicles.models import Vehicle


class Booking(models.Model):

    SERVICE_TYPE_CHOICES = [
        ('hour', 'Hourly'),
        ('day', 'Daily'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('active', 'On Service'),
        ('completed', 'Completed'),
        ('late', 'Late'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)

    service_type = models.CharField(max_length=10, choices=SERVICE_TYPE_CHOICES)

    booking_date = models.DateField()
    start_time = models.TimeField()

    # CONDITIONAL FIELDS (must allow NULL)
    hours = models.PositiveIntegerField(null=True, blank=True)
    days = models.PositiveIntegerField(null=True, blank=True)

    # Pickup confirmation
    user_confirmed_pickup = models.BooleanField(default=False)
    owner_confirmed_pickup = models.BooleanField(default=False)

    # Return confirmation
    user_confirmed_return = models.BooleanField(default=False)
    owner_confirmed_return = models.BooleanField(default=False)

    service_started_at = models.DateTimeField(null=True, blank=True)
    expected_end_at = models.DateTimeField(null=True, blank=True)
    actual_end_at = models.DateTimeField(null=True, blank=True)

    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    late_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='confirmed')
    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_expected_end(self):
        if not self.service_started_at:
            return None

        if self.service_type == 'hour' and self.hours:
            return self.service_started_at + timedelta(hours=self.hours)

        if self.service_type == 'day' and self.days:
            return self.service_started_at + timedelta(days=self.days)

        return None

    def start_service_if_ready(self):
        if (
            self.user_confirmed_pickup
            and self.owner_confirmed_pickup
            and not self.service_started_at
        ):
            self.service_started_at = timezone.now()
            self.expected_end_at = self.calculate_expected_end()
            self.status = 'active'
            self.save()

    def __str__(self):
        return f"{self.user.username} → {self.vehicle.vehicle_name} ({self.status})"

#-------------------------------Notification model--------------------------------- 
class Notification(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='notifications') 
    booking = models.ForeignKey(Booking,on_delete=models.CASCADE,related_name='notifications' )
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True) 
    def __str__(self):
        return f"Notification for {self.user.username} | Booking #{self.booking.id}"