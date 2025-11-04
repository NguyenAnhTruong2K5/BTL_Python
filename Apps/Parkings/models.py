from django.db import models

class Card(models.Model):
    card_id = models.CharField(primary_key=True, max_length=50)  # Mã thẻ hoặc QR
    status = models.CharField(max_length=20, default="available")  # available, in_use, lost, disabled

    def __str__(self):
        return self.card_id


class ParkingSlot(models.Model):
    slot_id = models.AutoField(primary_key=True)
    slot_code = models.CharField(max_length=20, unique=True)
    slot_type = models.CharField(max_length=20, default="car")  # car, motorbike
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.slot_code


class ParkingRecord(models.Model):
    record_id = models.AutoField(primary_key=True)
    card = models.ForeignKey(Card, on_delete=models.SET_NULL, null=True, related_name="parking_records")
    slot = models.ForeignKey(ParkingSlot, on_delete=models.SET_NULL, null=True, related_name="parking_records")
    entry_time = models.DateTimeField()
    exit_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Record {self.record_id} - {self.vehicle}"