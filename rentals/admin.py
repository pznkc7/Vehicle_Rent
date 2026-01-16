from django.contrib import admin

# Register your models here.

from .models import Rental_User
from vehicles.models import Vehicle
admin.site.register(Rental_User)




