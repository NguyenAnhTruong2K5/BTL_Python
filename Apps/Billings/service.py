import math
from django.utils import timezone
from Apps.Parkings.models import ParkingRecord
from Apps.Contracts.models import Contract
from .models import ParkingInvoice, Pricing


def calculate_fee_for_record(record_id):
    """
    Tính phí gửi xe dựa theo ParkingRecord và Contract (nếu có)
    """
    try:
        record = ParkingRecord.objects.get(id=record_id)
    except ParkingRecord.DoesNotExist:
        return {"error": "Không tìm thấy ParkingRecord."}

    if not record.check_in_time or not record.check_out_time:
        return {"error": "Lượt gửi xe chưa có đầy đủ thời gian check-in/out."}

    plate = record.plate_number
    veh_type = record.vehicle_type
    in_time = record.check_in_time
    out_time = record.check_out_time

    # Kiểm tra hợp đồng còn hạn
    contract = (
        Contract.objects.filter(plate_number=plate, end_date__gte=in_time, status='valid')
        .order_by('-end_date')
        .first()
    )

    # Xác định thời gian tính phí
    if contract:
        if out_time.date() <= contract.end_date:
            charge_minutes = 0
        elif in_time.date() >= contract.end_date:
            charge_minutes = (out_time - in_time).total_seconds() / 60
        else:
            # check_in < end_date < check_out
            end_dt = timezone.make_aware(
                timezone.datetime.combine(contract.end_date, timezone.datetime.min.time())
            )
            charge_minutes = (out_time - end_dt).total_seconds() / 60
    else:
        charge_minutes = (out_time - in_time).total_seconds() / 60

    # Làm tròn giờ lên
    hours_chargeable = math.ceil(charge_minutes / 60)

    # Lấy giá gửi theo giờ
    pricing = Pricing.objects.filter(vehicle_type=veh_type, term='hourly').first()
    rate = float(pricing.rate) if pricing else 0
    fee = hours_chargeable * rate

    return {
        "record": record,
        "contract": contract,
        "pricing": pricing,
        "fee": round(fee, 2)
    }
