from django.urls import path
from . import views

urlpatterns = [
    # ContractInvoice URLs
    path('contract_invoices/', views.ContractInvoiceListCreateView.as_view(), name='contract-invoice-list-create'),
    path('contract_invoices/<str:invoice_id>/', views.ContractInvoiceRetrieveUpdateView.as_view(), name='contract-invoice-detail'),
    path('contract_invoices/<str:invoice_id>/delete/', views.ContractInvoiceDestroyView.as_view(), name='contract-invoice-delete'),
    path('contract_invoices/search/', views.SearchContractInvoiceView.as_view(), name='contract-invoice-search'),

    # ParkingInvoice URLs
    path('parking_invoices/', views.ParkingInvoiceListCreateView.as_view(), name='parking-invoice-list-create'),
    path('parking_invoices/<str:invoice_id>/', views.ParkingInvoiceRetrieveUpdateView.as_view(), name='parking-invoice-detail'),
    path('parking_invoices/<str:invoice_id>/delete/', views.ParkingInvoiceDestroyView.as_view(), name='parking-invoice-delete'),
    path('parking_invoices/search/', views.SearchParkingInvoiceView.as_view(), name='parking-invoice-search'),
]
