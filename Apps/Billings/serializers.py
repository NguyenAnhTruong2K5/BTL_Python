from rest_framework import serializers
from django.utils import timezone
from .models import ContractInvoice, ParkingInvoice, Pricing
from Apps.Parkings.models import ParkingRecord
from Apps.Accounts.models import Contract
import math


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
def calculate_fee_for_record(record_id: int) -> float:
    try:
        record = ParkingRecord.objects.get(id=record_id)
    except ParkingRecord.DoesNotExist:
        return 0.0

    if not record.check_in_time:
        return 0.0

    end_time = record.check_out_time or timezone.now()

    contract = Contract.objects.filter(
        plate_number=record.plate_number,
        end_date__gte=record.check_in_time
    ).order_by('end_date').first()

    if contract:
        if end_time <= contract.end_date:
            charge_start = end_time  # fee = 0
        elif record.check_in_time >= contract.end_date:
            charge_start = record.check_in_time
        else:
            charge_start = contract.end_date
    else:
        charge_start = record.check_in_time

    delta = end_time - charge_start
    hours_chargeable = math.ceil(delta.total_seconds() / 3600)

    pricing = Pricing.objects.filter(
        vehicle_type=record.vehicle_type,
        term='hourly'
    ).first()

    rate = pricing.rate if pricing else 0
    fee = hours_chargeable * rate
    return fee

class ParkingInvoiceSummarySerializer(serializers.ModelSerializer):
    check_in_time = serializers.DateTimeField(
        source='record_id.check_in_time',
        format="%d/%m/%Y %H:%M", read_only=True
    )
    check_out_time = serializers.DateTimeField(
        source='record_id.check_out_time',
        format="%d/%m/%Y %H:%M", read_only=True
    )

    class Meta:
        model = ParkingInvoice
        fields = ['invoice_id', 'check_in_time', 'check_out_time', 'amount', 'payment_date']



class CreateParkingInvoiceSerializer(serializers.ModelSerializer):
    record_id = serializers.PrimaryKeyRelatedField(queryset=ParkingRecord.objects.all())

    class Meta:
        model = ParkingInvoice
        fields = ['record_id']

    def create(self, validated_data):
        record = validated_data.pop('record_id')
        if record.check_out_time is None:
            record.check_out_time = timezone.now()
            record.save()

        fee = calculate_fee_for_record(record.id)
        if fee <= 0:
            raise serializers.ValidationError(
                "Lượt gửi này nằm trong thời hạn hợp đồng, không cần thanh toán."
            )

        pricing = Pricing.objects.filter(
            vehicle_type=record.vehicle_type,
            term='hourly'
        ).first()

        invoice = ParkingInvoice.objects.create(
            record_id=record,
            pricing=pricing,
            amount=fee,
            payment_date=timezone.now()
        )
        return invoice


# Pricing

class PricingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pricing
        fields = ['pricing_id', 'vehicle_type', 'term', 'rate']
