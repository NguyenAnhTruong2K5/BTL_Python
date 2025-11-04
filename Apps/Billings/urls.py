from django.urls import path
from Apps.Billings import views  

urlpatterns = [
    # --- ContractInvoice URLs ---

    # Handles GET (list) and POST (create)
    path('contract_invoices/', views.ContractInvoiceListCreateView.as_view(), name='contract-invoice-list-create'),

    # Handles GET (search) on /contract_invoices/search/?search=...
    path('contract_invoices/search/', views.SearchContractInvoiceView.as_view(), name='contract-invoice-search'),

    # Handles PUT/PATCH on /contract_invoices/<pk>/update/
    path('contract_invoices/<str:pk>/update/', views.ContractInvoiceRetrieveUpdateView.as_view(), name='contract-invoice-update'),

    # Handles DELETE on /contract_invoices/<pk>/delete/
    path('contract_invoices/<str:pk>/delete/', views.ContractInvoiceDestroyView.as_view(), name='contract-invoice-delete'),

    # --- ParkingInvoice URLs ---

    # Handles GET (list) and POST (create)
    path('parking_invoices/', views.ParkingInvoiceListCreateView.as_view(), name='parking-invoice-list-create'),

    # Handles GET (search) on /parking_invoices/search/?search=...
    path('parking_invoices/search/', views.SearchParkingInvoiceView.as_view(), name='parking-invoice-search'),

    # Handles PUT/PATCH on /parking_invoices/<pk>/update/
    path('parking_invoices/<str:pk>/update/', views.ParkingInvoiceRetrieveUpdateView.as_view(), name='parking-invoice-update'),

    # Handles DELETE on /parking_invoices/<str:pk>/delete/
    path('parking_invoices/<str:pk>/delete/', views.ParkingInvoiceDestroyView.as_view(), name='parking-invoice-delete'),
]
