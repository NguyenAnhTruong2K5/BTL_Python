from django.contrib import admin
from .models import Card, ParkingRecord


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('id', 'status')  # chỉ còn 2 trường hợp lệ


@admin.register(ParkingRecord)
class ParkingRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'plate_number', 'vehicle_type', 'check_in_time', 'check_out_time')