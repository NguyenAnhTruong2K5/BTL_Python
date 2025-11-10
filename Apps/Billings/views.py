from rest_framework import generics, status
from rest_framework.response import Response
from .models import ContractInvoice, ParkingInvoice, Pricing
from .serializers import (
    ContractInvoiceSummarySerializer, CreateContractInvoiceSerializer,
    ParkingInvoiceSummarySerializer, CreateParkingInvoiceSerializer,
    PricingSerializer
)


# Contract_Invoice


class ContractInvoiceListCreateView(generics.ListCreateAPIView):
    queryset = ContractInvoice.objects.all()
    serializer_class = ContractInvoiceSummarySerializer  # rút gọn hiển thị

    def post(self, request, *args, **kwargs):
        serializer = CreateContractInvoiceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        invoice = serializer.save()
        return Response(
            ContractInvoiceSummarySerializer(invoice).data,
            status=status.HTTP_201_CREATED
        )


class ContractInvoiceRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = ContractInvoice.objects.all()
    serializer_class = ContractInvoiceSummarySerializer
    lookup_field = 'invoice_id'


class ContractInvoiceDestroyView(generics.DestroyAPIView):
    queryset = ContractInvoice.objects.all()
    serializer_class = ContractInvoiceSummarySerializer
    lookup_field = 'invoice_id'


# Parking_Invoice

class ParkingInvoiceListCreateView(generics.ListCreateAPIView):
    queryset = ParkingInvoice.objects.all()
    serializer_class = ParkingInvoiceSummarySerializer  # rút gọn hiển thị

    def post(self, request, *args, **kwargs):
        serializer = CreateParkingInvoiceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        invoice = serializer.save()
        return Response(
            ParkingInvoiceSummarySerializer(invoice).data,
            status=status.HTTP_201_CREATED
        )


class ParkingInvoiceRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = ParkingInvoice.objects.all()
    serializer_class = ParkingInvoiceSummarySerializer
    lookup_field = 'invoice_id'


class ParkingInvoiceDestroyView(generics.DestroyAPIView):
    queryset = ParkingInvoice.objects.all()
    serializer_class = ParkingInvoiceSummarySerializer
    lookup_field = 'invoice_id'


# Search

class SearchContractInvoiceView(generics.ListAPIView):
    serializer_class = ContractInvoiceSummarySerializer

    def get_queryset(self):
        search_term = self.request.GET.get('search', '')
        return ContractInvoice.objects.filter(invoice_id__icontains=search_term)


class SearchParkingInvoiceView(generics.ListAPIView):
    serializer_class = ParkingInvoiceSummarySerializer

    def get_queryset(self):
        search_term = self.request.GET.get('search', '')
        return ParkingInvoice.objects.filter(invoice_id__icontains=search_term)


# Pricing List

class PricingListView(generics.ListAPIView):
    queryset = Pricing.objects.all()
    serializer_class = PricingSerializer
