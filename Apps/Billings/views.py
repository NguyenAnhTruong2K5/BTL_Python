from rest_framework import generics, filters
from rest_framework.generics import get_object_or_404

from .models import ContractInvoice, ParkingInvoice, ParkingRecord, Pricing
from .serializers import (
    ContractInvoiceSerializer,
    ParkingInvoiceSerializer,
)
# Views for ContractInvoice

#1️ List + Create
class ContractInvoiceListCreateView(generics.ListCreateAPIView):
    queryset = ContractInvoice.objects.all()
    serializer_class = ContractInvoiceSerializer


#2️ Retrieve + Update
class ContractInvoiceRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = ContractInvoice.objects.all()
    serializer_class = ContractInvoiceSerializer


#3️ Delete
class ContractInvoiceDestroyView(generics.DestroyAPIView):
    queryset = ContractInvoice.objects.all()
    serializer_class = ContractInvoiceSerializer


#4️ Search (theo pricing_id hoặc invoice_id)
class SearchContractInvoiceView(generics.ListAPIView):
    queryset = ContractInvoice.objects.all()
    serializer_class = ContractInvoiceSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["invoice_id", "pricing_id__pricing_id"]

# Views for ParkingInvoice

#1️ List + Create
class ParkingInvoiceListCreateView(generics.ListCreateAPIView):
    queryset = ParkingInvoice.objects.all()
    serializer_class = ParkingInvoiceSerializer


#2️ Retrieve + Update
class ParkingInvoiceRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = ParkingInvoice.objects.all()
    serializer_class = ParkingInvoiceSerializer


#3️ Delete
class ParkingInvoiceDestroyView(generics.DestroyAPIView):
    queryset = ParkingInvoice.objects.all()
    serializer_class = ParkingInvoiceSerializer


#4️ Search (theo record_id hoặc invoice_id)
class SearchParkingInvoiceView(generics.ListAPIView):
    queryset = ParkingInvoice.objects.all()
    serializer_class = ParkingInvoiceSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["invoice_id", "record_id__record_id"]
