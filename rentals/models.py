from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Rental_User(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, blank=False)
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30)
    license_number = models.CharField(max_length=20, unique=True)
    phone_number =models.CharField(max_length=15)
    permanent_address = models.TextField()
    temporary_address = models.TextField(blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.license_number}"




