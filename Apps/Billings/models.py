from django.db import models
from django.utils import timezone

TERM_CHOICES = [
    ('hourly', 'Hourly'),
    ('monthly', 'Monthly'),
    ('yearly', 'Yearly'),
]

VEHICLE_TYPES = [
    ('motorbike', 'Motorbike'),
    ('car', 'Car'),
]

class Pricing(models.Model):
    pricing_id = models.CharField(max_length=50, primary_key=True, default='1')
    vehicle_type = models.CharField(max_length=100, choices=VEHICLE_TYPES, default='motorbike')
    term = models.CharField(max_length=10, choices=TERM_CHOICES, default='monthly')
    rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.rate or self.rate == 0:
            if self.vehicle_type == 'motorbike':
                if self.term == 'hourly':
                    self.rate = 3000
                elif self.term == 'monthly':
                    self.rate = 300000
                elif self.term == 'yearly':
                    self.rate = 800000
            elif self.vehicle_type == 'car':
                if self.term == 'hourly':
                    self.rate = 10000
                elif self.term == 'monthly':
                    self.rate = 1000000
                elif self.term == 'yearly':
                    self.rate = 2000000
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.vehicle_type} - {self.term} - {self.rate}"


class ContractInvoice(models.Model):
    invoice_id = models.CharField(max_length=30, primary_key=True, editable=False)
    pricing = models.ForeignKey(Pricing, on_delete=models.PROTECT, to_field='pricing_id', db_column='pricing_id')
    amount = models.DecimalField(max_digits=18, decimal_places=2)
    payment_date = models.DateTimeField(default=timezone.now)


    def save(self, *args, **kwargs):
        if not self.invoice_id:
            last_invoice = ContractInvoice.objects.order_by('-invoice_id').first()
            if last_invoice and last_invoice.invoice_id.startswith("CINV"):
                last_num = int(last_invoice.invoice_id[4:])
                new_num = last_num + 1
            else:
                new_num = 1
            self.invoice_id = f"CINV{new_num:06d}"
        super().save(*args, **kwargs)


class ParkingInvoice(models.Model):
    invoice_id = models.CharField(max_length=30, primary_key=True, editable=False)
    record = models.ForeignKey('Parkings.ParkingRecord', on_delete=models.CASCADE)
    pricing = models.ForeignKey(Pricing, on_delete=models.SET_NULL, null=True, blank=True,
                                to_field='pricing_id', db_column='pricing_id')
    amount = models.DecimalField(max_digits=18, decimal_places=2)
    payment_date = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.invoice_id:
            last_invoice = ParkingInvoice.objects.order_by('-invoice_id').first()
            if last_invoice and last_invoice.invoice_id.startswith("PINV"):
                last_num = int(last_invoice.invoice_id[4:])
                new_num = last_num + 1
            else:
                new_num = 1
            self.invoice_id = f"PINV{new_num:06d}"
        super().save(*args, **kwargs)
