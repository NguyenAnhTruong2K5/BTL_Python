from django.db import models
from django.utils import timezone


class Card(models.Model):
    STATUS_CHOICES = [('inactive', 'Inactive'), ('active', 'Active'), ('disable', 'Disabled'),]

    # id là mã thẻ
    id = models.BigAutoField(primary_key=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='inactive', db_column='status')

    class Meta:
        db_table = 'Parkings_card'

    def __str__(self):
        return f"{self.id} ({self.status})"


class ParkingRecord(models.Model):
    VEHICLE_TYPE_CHOICES = [('motorbike', 'Motorbike'), ('car', 'Car'),]

    id = models.BigAutoField(primary_key=True, db_column='id')
    card = models.ForeignKey(Card, on_delete=models.CASCADE, db_column='card_id')
    plate_number = models.CharField(max_length=20, db_column='plate_number')
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPE_CHOICES, db_column='vehicle_type')
    check_in_time = models.DateTimeField(auto_now_add=True, db_column='check_in_time')
    check_out_time = models.DateTimeField(null=True, blank=True, db_column='check_out_time')
    image_path = models.CharField(max_length=255, null=True, blank=True, db_column='image_path')

    class Meta:
        db_table = 'Parkings_parkingrecord'

    def __str__(self):
        return f"{self.plate_number} - {self.card.id}"

    @property
    def is_active(self):
        return self.check_out_time is None