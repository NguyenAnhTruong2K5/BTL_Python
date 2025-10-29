
from rest_framework import generics, filters
from rest_framework.generics import get_object_or_404

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
    def perform_create(self, serializer):
        customer_cccd = self.kwargs['cccd']
        customer_instance = get_object_or_404(Customer, cccd= customer_cccd)
        serializer.save(cccd= customer_instance)

class ListContractView(generics.ListAPIView):
    serializer_class = ListContractSerializer
    def get_queryset(self):
        customer_cccd = self.kwargs['cccd']
        query_set = Contract.objects.all().filter(cccd_id= customer_cccd)
        return query_set

class SearchContractView(generics.ListAPIView):
    queryset = Contract.objects.all()
    serializer_class = ListContractSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["cccd__cccd", "plate_number",]


class UpdateContractView(generics.RetrieveUpdateAPIView):
    queryset = Contract.objects.all()
    serializer_class = UpdateContractSerializer


class DeleteContractView(generics.DestroyAPIView):
    queryset = Contract.objects.all()
    serializer_class = DeleteContractSerializer

