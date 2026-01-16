from django.contrib import admin

# Register your models here.
from bookings.models import Booking
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'vehicle', 'service_started_at', 'status', 'total_price', 'fine_amount')
    list_filter = ('vehicle',)
