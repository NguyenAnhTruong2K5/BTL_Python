from django.contrib import admin
from .models import Customer, Contract

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('cccd', 'name', 'email', 'phone_number')
    search_fields = ('cccd', 'name', 'email', 'phone_number')
    ordering = ('-name', )

@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ('plate_number', "vehicle_type", 'term', 'duration', 'start_date', 'end_date', )
    search_fields = ('start_date', 'end_date', )
    list_filter = ('term', 'duration', )
    ordering = ('-start_date', )
    readonly_fields = ('start_date', 'end_date')

    # This organizes your add/edit page
    fieldsets = (
        (None, {
            'fields': ('plate_number', 'cccd', 'term', 'duration', 'vehicle_type')
        }),
        ('Calculated Dates (Read-Only)', {
            'fields': ('start_date', 'end_date')
        }),
    )
