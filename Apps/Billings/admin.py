
from django.contrib import admin
from .models import Pricing, ContractInvoice, ParkingInvoice

# Hiển thị Pricing
@admin.register(Pricing)
class PricingAdmin(admin.ModelAdmin):
    list_display = ('pricing_id', 'vehicle_type', 'term', 'rate')
    search_fields = ('pricing_id', 'vehicle_type')

# Hiển thị ContractInvoice
@admin.register(ContractInvoice)
class ContractInvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_id', 'pricing_id', 'amount', 'payment_date')
    search_fields = ('invoice_id', 'pricing_id__pricing_id')
    list_filter = ('payment_date',)

# Hiển thị ParkingInvoice
@admin.register(ParkingInvoice)
class ParkingInvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_id', 'record_id', 'pricing', 'amount', 'payment_date')
    search_fields = ('invoice_id', 'record_id__record_id', 'pricing__pricing_id')
    list_filter = ('payment_date',)
