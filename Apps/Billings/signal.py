from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from datetime import datetime
from Apps.Accounts.models import *
from Apps.Parkings.models import ParkingRecord
from .models import *

@receiver(post_save, sender=Contract)
def create_invoice(sender, instance, created, **kwargs):
    if created:
        contract = instance
        pricing_instance = get_object_or_404(Pricing, vehicle_type=contract.vehicle_type, term=contract.term)
        contract_invoice = ContractInvoice.objects.create(
            plate_number_id= contract.plate_number,
            pricing_id= pricing_instance,
            amount= pricing_instance.rate * contract.duration
        )
        contract_invoice.save()

@receiver(post_save, sender= ParkingRecord)
def create_parking_record(sender, instance, created, **kwargs):
    if created:
        parking_record = instance
        pricing_instance = get_object_or_404(Pricing, vehicle_type= parking_record.vehicle_type, term= 'hourly')
        check_in_time = datetime(parking_record.check_in_time)
        check_out_time = datetime(parking_record.check_out_time)
        delta = check_out_time - check_in_time
        hours = delta.total_seconds() / 3600
        parking_invoice = ParkingInvoice.objects.create(
            record_id_id= parking_record.id,
            pricing_id= pricing_instance,
            amount= hours * pricing_instance.rate,
            payment_date= datetime(check_out_time)
        )
        parking_invoice.save()


