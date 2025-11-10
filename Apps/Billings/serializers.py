from rest_framework import serializers
from django.utils import timezone
from .models import ContractInvoice, ParkingInvoice, Pricing
from Apps.Parkings.models import ParkingRecord


# Contract_Invoice


class ContractInvoiceSummarySerializer(serializers.ModelSerializer):
    payment_date = serializers.DateTimeField(format="%d/%m/%Y %H:%M", read_only=True)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = ContractInvoice
        fields = ['invoice_id', 'amount', 'payment_date']


class CreateContractInvoiceSerializer(serializers.ModelSerializer):
    pricing = serializers.PrimaryKeyRelatedField(
        queryset=Pricing.objects.all()
    )

    class Meta:
        model = ContractInvoice
        fields = ['pricing']

    def create(self, validated_data):
        pricing = validated_data.pop('pricing')

        if pricing.term == 'monthly':
            amount = pricing.rate
        elif pricing.term == 'yearly':
            amount = pricing.rate * 12
        else:
            amount = pricing.rate

        invoice = ContractInvoice.objects.create(
            pricing=pricing,
            amount=amount,
            payment_date=timezone.now()
        )
        return invoice



# Parking_Invoice


class ParkingInvoiceSummarySerializer(serializers.ModelSerializer):
    payment_date = serializers.DateTimeField(format="%d/%m/%Y %H:%M", read_only=True)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = ParkingInvoice
        fields = ['invoice_id', 'amount', 'payment_date']


class CreateParkingInvoiceSerializer(serializers.ModelSerializer):
    record = serializers.PrimaryKeyRelatedField(queryset=ParkingRecord.objects.all())
    pricing = serializers.PrimaryKeyRelatedField(queryset=Pricing.objects.all())

    class Meta:
        model = ParkingInvoice
        fields = ['record', 'pricing']

    def create(self, validated_data):
        record = validated_data.pop('record')
        pricing = validated_data.pop('pricing')

        if record.check_out_time and record.check_in_time:
            duration = (record.check_out_time - record.check_in_time).total_seconds() / 3600
        else:
            duration = 0

        amount = round(duration * float(pricing.rate), 2)

        invoice = ParkingInvoice.objects.create(
            record=record,
            pricing=pricing,
            amount=amount,
            payment_date=timezone.now()
        )
        return invoice


# Pricing

class PricingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pricing
        fields = ['pricing_id', 'vehicle_type', 'term', 'rate']
