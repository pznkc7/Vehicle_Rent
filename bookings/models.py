from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from vehicles.models import Vehicle
from datetime import timedelta

# bookings/models.py
class Booking(models.Model):
    SERVICE_TYPE_CHOICES = (
        ('hour', 'Hourly'),
        ('day', 'Daily'),
    )

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('active', 'On Service'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)

    service_type = models.CharField(max_length=10, choices=SERVICE_TYPE_CHOICES)
    total_hours = models.PositiveIntegerField(null=True, blank=True)
    total_days = models.PositiveIntegerField(null=True, blank=True)

    booking_date = models.DateTimeField(auto_now_add=True)
    service_started_at = models.DateTimeField(null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    fine_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def expected_end_time(self):
        if not self.service_started_at:
            return None
        if self.service_type == 'hour':
            return self.service_started_at + timedelta(hours=self.total_hours)
        return self.service_started_at + timedelta(days=self.total_days)
