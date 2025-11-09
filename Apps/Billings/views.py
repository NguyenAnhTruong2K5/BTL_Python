from rest_framework import generics, status
from rest_framework.response import Response
from .models import Contract_Invoice, Parking_Invoice
from .serializers import (
    ContractInvoiceSerializer,
    CreateContractInvoiceSerializer,
    ParkingInvoiceSerializer,
    CreateParkingInvoiceSerializer,
)



# Contract invoice

class ContractInvoiceListCreateView(generics.ListCreateAPIView):
    queryset = Contract_Invoice.objects.all()
    serializer_class = ContractInvoiceSerializer

    def post(self, request, *args, **kwargs):
        serializer = CreateContractInvoiceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        invoice = serializer.save()
        return Response(
            {
                "invoice": ContractInvoiceSerializer(invoice).data
            },
            status=status.HTTP_201_CREATED
        )


class ContractInvoiceRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Contract_Invoice.objects.all()
    serializer_class = ContractInvoiceSerializer
    lookup_field = 'invoice_id'


class ContractInvoiceDestroyView(generics.DestroyAPIView):
    queryset = Contract_Invoice.objects.all()
    serializer_class = ContractInvoiceSerializer
    lookup_field = 'invoice_id'


class SearchContractInvoiceView(generics.ListAPIView):
    serializer_class = ContractInvoiceSerializer

    def get_queryset(self):
        search_term = self.request.GET.get('search', '')
        return Contract_Invoice.objects.filter(pricing__pricing_id__icontains=search_term)


# Parking Invoice

class ParkingInvoiceListCreateView(generics.ListCreateAPIView):
    queryset = Parking_Invoice.objects.all()
    serializer_class = ParkingInvoiceSerializer

    def post(self, request, *args, **kwargs):
        serializer = CreateParkingInvoiceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        invoice = serializer.save()
        return Response(
            {
                "invoice": ParkingInvoiceSerializer(invoice).data
            },
            status=status.HTTP_201_CREATED
        )


class ParkingInvoiceRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Parking_Invoice.objects.all()
    serializer_class = ParkingInvoiceSerializer
    lookup_field = 'invoice_id'


class ParkingInvoiceDestroyView(generics.DestroyAPIView):
    queryset = Parking_Invoice.objects.all()
    serializer_class = ParkingInvoiceSerializer
    lookup_field = 'invoice_id'


class SearchParkingInvoiceView(generics.ListAPIView):
    serializer_class = ParkingInvoiceSerializer

    def get_queryset(self):
        search_term = self.request.GET.get('search', '')
        return Parking_Invoice.objects.filter(record__record_id__icontains=search_term)
