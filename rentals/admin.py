from django.contrib import admin

# Register your models here.

from .models import Rental_User
from vehicles.models import Vehicle, Booking

admin.site.register(Rental_User)




@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'vehicle', 'start_date', 'end_date')
    list_filter = ('vehicle',)
