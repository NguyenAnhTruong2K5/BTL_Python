from django.urls import path
from Apps.Billings import views

urlpatterns = [
    # Contract Invoice
    path('contract-invoices/', views.ContractInvoiceListCreateView.as_view(), name='contract-invoice-list-create'),
    path('contract-invoices/<str:invoice_id>/', views.ContractInvoiceRetrieveUpdateView.as_view(), name='contract-invoice-detail'),
    path('contract-invoices/<str:invoice_id>/delete/', views.ContractInvoiceDestroyView.as_view(), name='contract-invoice-delete'),
    path('contract-invoices/search/', views.SearchContractInvoiceView.as_view(), name='contract-invoice-search'),

    # Parking Invoice
    path('parking-invoices/', views.ParkingInvoiceListCreateView.as_view(), name='parking-invoice-list-create'),
    path('parking-invoices/<str:invoice_id>/', views.ParkingInvoiceRetrieveUpdateView.as_view(), name='parking-invoice-detail'),
    path('parking-invoices/<str:invoice_id>/delete/', views.ParkingInvoiceDestroyView.as_view(), name='parking-invoice-delete'),
    path('parking-invoices/search/', views.SearchParkingInvoiceView.as_view(), name='parking-invoice-search'),
]