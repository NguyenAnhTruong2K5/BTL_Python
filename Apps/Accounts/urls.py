from django.urls import path
from Apps.Accounts import views

urlpatterns = [
    path('', views.customer_list, name='customer-list-page'),
    path('customers/new/', views.customer_create, name='customer-create-page'),
    path('customers/<str:pk>/edit/', views.customer_update, name='customer-update-page'),
    path('contracts/', views.contract_list, name='contract-list-page'),
    path('contracts/new/', views.contract_create, name='contract-create-page'),
    path('contracts/<str:pk>/edit/', views.contract_update, name='contract-update-page'),
    path('statistics/', views.statistics, name='statistics-page'),
]
