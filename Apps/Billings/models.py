from django.db import models
from dateutil.relativedelta import MO, relativedelta
from django.utils import timezone

class Pricing(models.Model):
    VEHICLE_CHOICES = [
        ('motorbike', 'Motorbike'),
        ('car', 'Car'),
    ]

    TERM_CHOICES = [
        ('hourly', 'Hourly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]

    pricing_id = models.CharField(max_length=50, primary_key=True, default='1')
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_CHOICES)
    term = models.CharField(max_length=10, choices=TERM_CHOICES)
    rate = models.DecimalField(max_digits=18, decimal_places=2)

class Contract_Invoice(models.Model):
    invoice_id = models.CharField(max_length=30, primary_key= True,editable=False)
    pricing_id = models.ForeignKey('Pricing', on_delete=models.CASCADE, to_field='pricing_id', db_column='pricing_id')
    amount = models.DecimalField(max_digits=18, decimal_places=2)
    payment_date = models.DateTimeField(default=timezone.now)
    
    def save(self, *args, **kwargs):
        if not self.invoice_id:
            last_invoice = Contract_Invoice.objects.order_by('-invoice_id').first()
            if last_invoice and last_invoice.invoice_id.startswith("CINV"):
                last_num = int(last_invoice.invoice_id[4:])
                new_num = last_num + 1
            else:
                new_num = 1
            self.invoice_id = f"CINV{new_num:06d}"
        super().save(*args, **kwargs)


class Parking_Invoice(models.Model):
    invoice_id = models.CharField(max_length=30, primary_key= True,editable=False)
    record_id = models.ForeignKey('Parkings.ParkingRecord', on_delete=models.CASCADE)
    pricing = models.ForeignKey('Pricing',on_delete=models.SET_NULL,null=True,blank=True, to_field='pricing_id', db_column='pricing_id')
    amount = models.DecimalField(max_digits=18, decimal_places=2)
    payment_date = models.DateTimeField(default=timezone.now)



    def save(self, *args, **kwargs):
        if not self.invoice_id:
            last_invoice = Contract_Invoice.objects.order_by('-invoice_id').first()
            if last_invoice and last_invoice.invoice_id.startswith("PINV"):
                last_num = int(last_invoice.invoice_id[4:])
                new_num = last_num + 1
            else:
                new_num = 1
            self.invoice_id = f"PINV{new_num:06d}"
        super().save(*args, **kwargs)