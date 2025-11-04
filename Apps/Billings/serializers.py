from rest_framework import serializers
from .models import ContractInvoice, ParkingInvoice, Contract, ParkingRecord, Pricing

# Contract Invoice
class ContractInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractInvoice
        fields = '__all__'


class CreateContractInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractInvoice
        fields = ['pricing', 'amount']

    def create(self, validated_data):
        invoice = ContractInvoice.objects.create(**validated_data)
        return invoice


# Parking Invoice

class ParkingInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingInvoice
        fields = '__all__'


class CreateParkingInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingInvoice
        fields = ['record', 'pricing', 'amount']

    def create(self, validated_data):
        invoice = ParkingInvoice.objects.create(**validated_data)
        return invoice
