from django import forms
from .models import ContractInvoice, ParkingInvoice

class ContractInvoiceForm(forms.ModelForm):
    class Meta:
        model = ContractInvoice
        fields = ['pricing_id', 'amount']

class ParkingInvoiceForm(forms.ModelForm):
    class Meta:
        model = ParkingInvoice
        fields = ['record_id', 'pricing', 'amount']
