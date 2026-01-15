from django.contrib import admin

# Register your models here.

from vehicles.models import  Vehicle, Booking
from django.contrib import admin
from .models import Vehicle


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = (
        'vehicle_name',
        'vehicle_type',
        'owner',
        'status',
        'is_available',
        'price_per_day',
        'created_at'
    )

    list_filter = ('status', 'vehicle_type', 'is_available')
    search_fields = ('vehicle_name', 'owner__username', 'pickup_address')

    actions = ['approve_vehicles', 'reject_vehicles']

    def approve_vehicles(self, request, queryset):
        queryset.update(status='approved', is_available=True)

    approve_vehicles.short_description = "Approve selected vehicles"

    def reject_vehicles(self, request, queryset):
        queryset.update(status='rejected', is_available=False)

    reject_vehicles.short_description = "Reject selected vehicles"



