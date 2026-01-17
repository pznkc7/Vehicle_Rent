from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'user',
        'vehicle',
        'service_type',
        'booking_date',
        'start_time',
        'status',
        'total_price',
        'late_fee',
        'created_at',
    )

    list_filter = (
        'service_type',
        'status',
        'booking_date',
    )

    search_fields = (
        'user__username',
        'vehicle__vehicle_name',
    )

    readonly_fields = (
        'total_price',
        'late_fee',
        'expected_end_at',
        'actual_end_at',
        'created_at',
    )

    ordering = ('-created_at',)
