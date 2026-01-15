from django.db import models
from django.contrib.auth.models import User

# Create your models here.

from django.db import models
from django.contrib.auth.models import User


class Vehicle(models.Model):
    VEHICLE_TYPE_CHOICES = [
        ('car', 'Car'),
        ('bike', 'Bike'),
        ('suv', 'SUV'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='vehicles',
        null=True,          # keep for now to avoid migration issues
        blank=True
    )

    vehicle_name = models.CharField(max_length=100)
    vehicle_type = models.CharField(max_length=10, choices=VEHICLE_TYPE_CHOICES)

    # Pricing
    price_per_hour = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        null=True,
        blank=True
    )

    price_per_day = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True
    )

    # Pickup location (NEW)
    pickup_address = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )

    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )

    image = models.ImageField(upload_to='vehicles/')
    description = models.TextField(null=True, blank=True)

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending'
    )

    is_available = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.vehicle_name} ({self.status})"



class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} → {self.vehicle.vehicle_name}"
