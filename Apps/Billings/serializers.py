from rest_framework import serializers
from django.utils import timezone
from .models import Contract_Invoice, Parking_Invoice, Pricing
from Apps.Parkings.models import ParkingRecord

# Contract Invoice

class ContractInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract_Invoice
        fields = '__all__'


class CreateContractInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract_Invoice
        fields = ['pricing']

    def create(self, validated_data):
        pricing = validated_data['pricing']

        if pricing.term == 'monthly':
            amount = pricing.rate
        elif pricing.term == 'yearly':
            amount = pricing.rate * 12
        else:
            amount = pricing.rate

        invoice = Contract_Invoice.objects.create(
            pricing=pricing,
            amount=amount,
            payment_date=timezone.now()
        )
        return invoice



# Parking Invoice

class ParkingInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parking_Invoice
        fields = '__all__'


class CreateParkingInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parking_Invoice
        fields = ['record', 'pricing']

    def create(self, validated_data):
        record = validated_data['record']
        pricing = validated_data['pricing']

        if record.exit_time and record.entry_time:
            duration = (record.exit_time - record.entry_time).total_seconds() / 3600
        else:
            duration = 0

        amount = round(duration * float(pricing.rate), 2)

        invoice = Parking_Invoice.objects.create(
            record=record,
            pricing=pricing,
            amount=amount,
            payment_date=timezone.now()
        )
        return invoice
