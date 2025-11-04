from rest_framework import serializers
from .models import Customer, Contract
from django.utils import timezone
#Serializers for Customer:
class ListCreateRetrieveDestroyCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class UpdateCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["phone_number", "email"]
#Serializers for Contract:
class CreateContractSerializer(serializers.ModelSerializer):
    cccd = serializers.SlugRelatedField(
        slug_field= 'cccd',
        read_only= True
    )

    class Meta:
        model = Contract
        fields = ['cccd', 'plate_number', 'vehicle_type', 'term', 'duration']


class ListContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        exclude = ["cccd"]
        def get_status(self, obj):
            if obj.end_date < timezone.now():
                return 'expired'
            return obj.status


class UpdateContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = ["term", "duration"]


class DeleteContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = "__all__"



