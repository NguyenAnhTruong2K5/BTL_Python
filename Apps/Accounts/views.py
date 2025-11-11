from django.shortcuts import render, redirect
from rest_framework import generics, filters
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination

from .serializers import *
from .models import Customer, Contract

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

#Views for Customer:
class CustomerListView(generics.ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = ListRetrieveDestroyCustomerSerializer
    pagination_class = StandardResultsSetPagination

class CustomerDestroyView(generics.DestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = ListRetrieveDestroyCustomerSerializer


class UpdateCustomerView(generics.RetrieveUpdateAPIView):
    queryset = Customer.objects.all()
    serializer_class = UpdateCustomerSerializer


class CreateCustomerView(generics.CreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CreateCustomerSerializer


class SearchCustomerView(generics.ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = ListRetrieveDestroyCustomerSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["cccd", "phone_number", "name"]

#Views for Contract:
class CreateContractView(generics.CreateAPIView):
    queryset = Contract.objects.all()
    serializer_class = CreateContractSerializer
    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        customer_cccd = self.kwargs['cccd']
        customer_instance = get_object_or_404(Customer, cccd= customer_cccd)
        serializer.save(cccd= customer_instance)

class ListContractView(generics.ListAPIView):
    queryset = Contract.objects.all()
    serializer_class = ListContractSerializer
    pagination_class = StandardResultsSetPagination

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



def statistics(request):
    # Tổng số khách hàng
    total_customers = Customer.objects.count()
    
    # Tổng số hợp đồng và phân loại
    total_contracts = Contract.objects.count()
    monthly_contracts = Contract.objects.filter(term='monthly').count()
    yearly_contracts = Contract.objects.filter(term='yearly').count()
    
    # Số hợp đồng theo trạng thái
    valid_contracts = Contract.objects.filter(status='valid').count()
    invalid_contracts = Contract.objects.filter(status='invalid').count()
    
    context = {
        'total_customers': total_customers,
        'total_contracts': total_contracts,
        'contract_types': {
            'monthly': monthly_contracts,
            'yearly': yearly_contracts
        },
        'contract_status': {
            'valid': valid_contracts,
            'invalid': invalid_contracts
        }
    }
    return render(request, 'accounts/statistics.html', context)
# Template Views
def customer_list(request):
    return render(request, 'accounts/customer/list.html')

def customer_create(request):
    return render(request, 'accounts/customer/create.html')

def customer_update(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    return render(request, 'accounts/customer/update.html', {'customer': customer})

def contract_list(request):
    return render(request, 'accounts/contract/list.html')

def contract_create(request):
    return render(request, 'accounts/contract/create.html')

def contract_update(request, pk):
    contract = get_object_or_404(Contract, pk=pk)
    return render(request, 'accounts/contract/update.html', {'contract': contract})