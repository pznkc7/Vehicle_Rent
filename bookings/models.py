from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta

from vehicles.models import Vehicle
# Create your models here.
from django.db import models
from datetime import timedelta
from django.contrib.auth.models import User
from vehicles.models import Vehicle
from django.utils import timezone

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

    hours = models.PositiveIntegerField()
    days = models.PositiveIntegerField()

    user_confirmed_pickup = models.BooleanField(default=False)
    owner_confirmed_pickup = models.BooleanField(default=False)

    service_started_at = models.DateTimeField()
    expected_end_at = models.DateTimeField()
    actual_end_at = models.DateTimeField()

    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    late_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='confirmed')
    created_at = models.DateTimeField(auto_now_add=True) 

    def start_service_if_ready(self):
        if self.user_confirmed_pickup and self.owner_confirmed_pickup and not self.service_started_at:
            now = timezone.now()
            self.service_started_at = now

            if self.service_type == 'hour':
                self.expected_end_at = now + timedelta(hours=self.hours)
            else:
                self.expected_end_at = now + timedelta(days=self.days)

            self.status = 'active'
            self.save()

    def __str__(self):
        return f"{self.user.username} → {self.vehicle.vehicle_name} ({self.status})"
