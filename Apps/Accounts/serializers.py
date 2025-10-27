from rest_framework import serializers
from .models import Customer, Contract

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
    class Meta:
        model = Contract
        fields = ['plate_number', 'vehicle_type', 'term', 'duration']


class ListContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        exclude = ["cccd"]


class UpdateContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = ["term", "duration"]


class DeleteContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = "__all__"



