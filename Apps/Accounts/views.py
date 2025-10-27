from rest_framework import generics, filters
from .serializers import *
from .models import Customer, Contract

#Views for Customer:
class CustomerListCreateView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = ListCreateRetrieveDestroyCustomerSerializer


class CustomerDestroyView(generics.DestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = ListCreateRetrieveDestroyCustomerSerializer


class UpdateCustomerView(generics.RetrieveUpdateAPIView):
    queryset = Customer.objects.all()
    serializer_class = UpdateCustomerSerializer


class SearchCustomerView(generics.ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = ListCreateRetrieveDestroyCustomerSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["cccd", "phone_number", "name"]

#Views for Contract:
class CreateContractView(generics.CreateAPIView):
    queryset = Contract.objects.all()
    serializer_class = CreateContractSerializer


class ListContractView(generics.ListAPIView):
    queryset = Contract.objects.all()
    serializer_class = ListContractSerializer


class SearchContractView(generics.ListAPIView):
    queryset = Contract.objects.all()
    serializer_class = ListContractSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["plate_number", "vehicle_type"]


class UpdateContractView(generics.RetrieveUpdateAPIView):
    queryset = Contract.objects.all()
    serializer_class = UpdateContractSerializer


class DeleteContractView(generics.DestroyAPIView):
    queryset = Contract.objects.all()
    serializer_class = DeleteContractSerializer

