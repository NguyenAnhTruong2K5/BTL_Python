from django.db import models
from Apps.Accounts.models import Customer

class Vehicle(models.Model):
    vehicle_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, related_name="vehicles")
    license_plate = models.CharField(max_length=20, unique=True)
    vehicle_type = models.CharField(max_length=20)  # car, motorbike

    def __str__(self):
        return self.license_plate