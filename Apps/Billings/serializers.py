from rest_framework import serializers
from django.utils import timezone
from .models import ContractInvoice, ParkingInvoice, Pricing, ParkingRecord


class PricingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pricing
        fields = ['pricing_id', 'vehicle_type', 'term', 'rate']


class ContractInvoiceSerializer(serializers.ModelSerializer):
    pricing = PricingSerializer(source='pricing_id', read_only=True)

    class Meta:
        model = ContractInvoice
        fields = ['invoice_id', 'pricing_id', 'pricing', 'amount', 'payment_date']


class ParkingRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingRecord
        fields = ['record_id', 'plate_number', 'vehicle_type', 'check_in_time', 'check_out_time']


class ParkingInvoiceSerializer(serializers.ModelSerializer):
    record = ParkingRecordSerializer(source='record_id', read_only=True)
    pricing = PricingSerializer(source='pricing_id', read_only=True)

    class Meta:
        model = ParkingInvoice
        fields = ['invoice_id', 'record_id', 'record', 'pricing_id', 'pricing', 'amount', 'payment_date']
