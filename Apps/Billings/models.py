from django.db import models
from Apps.Parkings.models import ParkingRecord

class Pricing(models.Model):
    price_id = models.AutoField(primary_key=True)
    vehicle_type = models.CharField(max_length=20)  # car, motorbike
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.vehicle_type} - {self.price_per_hour}/h"


class Invoice(models.Model):
    invoice_id = models.AutoField(primary_key=True)
    parking_record = models.OneToOneField(ParkingRecord, on_delete=models.CASCADE, related_name="invoice")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invoice {self.invoice_id}"