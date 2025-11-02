from django.urls import path
from Apps.Accounts import views

#API =
urlpatterns = [
    # -- Customer urls --

    # Handles CREATE on /customers/<cccd>/contracts/create
    path('customers/<str:cccd>/contracts/create/',
         views.CreateContractView.as_view(),
         name='create-contract-for-customer'),
    # Handles LIST on /customers/<cccd>/contracts/list
    path('customers/<str:cccd>/contracts/list/', views.ListContractView.as_view(), name= 'contract-list'),
    # Handles GET (list) and POST (create)
    path('customers/', views.CustomerListView.as_view(), name='customer-list-create'),
    path('customers/create', views.CreateCustomerView.as_view(), name= 'create-customer'),
    # Handles DELETE on /customers/<pk>/delete/
    path('customers/<str:pk>/delete/', views.CustomerDestroyView.as_view(), name='customer-destroy'),

    # Handles PUT/PATCH on /customers/<pk>/update/
    path('customers/<str:pk>/update/', views.UpdateCustomerView.as_view(), name='customer-update'),

    # Handles GET on /customers/search/?search=...
    path('customers/search/', views.SearchCustomerView.as_view(), name='customer-search'),

    # --- Contract URLs ---

    # Handles GET (list) on /contracts/
    path('contracts/', views.ListContractView.as_view(), name='contract-list'),

    # Handles GET on /contracts/search/?search=...
    path('contracts/search/', views.SearchContractView.as_view(), name='contract-search'),

    # Handles PUT/PATCH on /contracts/<pk>/update/
    path('contracts/<str:pk>/update/', views.UpdateContractView.as_view(), name='contract-update'),

    # Handles DELETE on /contracts/<pk>/delete/
    path('contracts/<str:pk>/delete/', views.DeleteContractView.as_view(), name='contract-delete'),
    
]
