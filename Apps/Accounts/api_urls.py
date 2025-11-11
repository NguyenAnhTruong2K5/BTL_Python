from django.urls import path
from Apps.Accounts import views

urlpatterns = [
    # -- Customer API urls --
    path('customers/<str:cccd>/contracts/create/',
         views.CreateContractView.as_view(),
         name='create-contract-for-customer'),
    path('customers/<str:cccd>/contracts/list/', 
         views.ListContractView.as_view(), 
         name='contract-list'),
    path('customers/', 
         views.CustomerListView.as_view(), 
         name='customer-list-create'),
    path('customers/create/', 
         views.CreateCustomerView.as_view(), 
         name='create-customer'),
    path('customers/<str:pk>/delete/', 
         views.CustomerDestroyView.as_view(), 
         name='customer-destroy'),
    path('customers/<str:pk>/update/', 
         views.UpdateCustomerView.as_view(), 
         name='customer-update'),
    path('customers/search/', 
         views.SearchCustomerView.as_view(), 
         name='customer-search'),

    # --- Contract API URLs ---
    path('contracts/', 
         views.ListContractView.as_view(), 
         name='contract-list'),
    path('contracts/search/', 
         views.SearchContractView.as_view(), 
         name='contract-search'),
    path('contracts/<str:pk>/update/', 
         views.UpdateContractView.as_view(), 
         name='contract-update'),
    path('contracts/<str:pk>/delete/', 
         views.DeleteContractView.as_view(), 
         name='contract-delete'),
]