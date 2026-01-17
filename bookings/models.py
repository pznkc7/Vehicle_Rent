from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta

from vehicles.models import Vehicle


class Booking(models.Model):

    # -------------------- CHOICES --------------------
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

    # -------------------- RELATIONS --------------------
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bookings'
    )

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name='bookings'
    )

    # -------------------- BOOKING INFO --------------------
    service_type = models.CharField(
        max_length=10,
        choices=SERVICE_TYPE_CHOICES
    )

    booking_date = models.DateField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)

    hours = models.PositiveIntegerField(null=True, blank=True)
    days = models.PositiveIntegerField(null=True, blank=True)

    # -------------------- TIME TRACKING --------------------
    expected_end_at = models.DateTimeField(null=True, blank=True)
    actual_end_at = models.DateTimeField(null=True, blank=True)

    # -------------------- PAYMENT --------------------
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    late_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    # -------------------- STATUS --------------------
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    # -------------------- CORE LOGIC --------------------
    def calculate_expected_end(self):
        """
        Calculates expected_end_at based on service type
        """
        start_dt = datetime.combine(self.booking_date, self.start_time)

        if self.service_type == 'hour' and self.hours:
            return start_dt + timedelta(hours=self.hours)

        if self.service_type == 'day' and self.days:
            return start_dt + timedelta(days=self.days)

        return None

    def is_late(self):
        """
        Checks if booking is late (used in admin & frontend)
        """
        if self.status != 'active' or not self.expected_end_at:
            return False
        return timezone.now() > self.expected_end_at

    def remaining_time(self):
        """
        Remaining time for frontend countdown
        """
        if self.status != 'active' or not self.expected_end_at:
            return None
        return self.expected_end_at - timezone.now()

    def save(self, *args, **kwargs):
        """
        Auto-set expected_end_at safely
        """
        if not self.expected_end_at:
            self.expected_end_at = self.calculate_expected_end()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} → {self.vehicle.vehicle_name} ({self.status})"
