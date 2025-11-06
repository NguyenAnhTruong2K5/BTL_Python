from django import forms
from .models import Card, ParkingRecord

class CheckInForm(forms.Form):
    card = forms.ModelChoiceField(
        queryset=Card.objects.filter(status='inactive'),
        label="Chọn thẻ khả dụng",
        required=True
    )
    plate_image = forms.ImageField(label="Ảnh biển số (từ AI)", required=True)


class CheckOutForm(forms.Form):
    card = forms.ModelChoiceField(
        queryset=Card.objects.filter(status='active'),
        label="Chọn thẻ đang active",
        required=True
    )
    plate_image = forms.ImageField(label="Ảnh biển số (từ AI)", required=True)


class LostCardForm(forms.Form):
    card_id = forms.CharField(label="Mã thẻ bị mất", required=True)


class HistoryFilterForm(forms.Form):
    from_date = forms.DateTimeField(label="Từ ngày", required=False, widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    to_date = forms.DateTimeField(label="Đến ngày", required=False, widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))