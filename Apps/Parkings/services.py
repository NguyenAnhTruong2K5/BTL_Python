from django.utils import timezone
from django.conf import settings
from .models import Card, ParkingRecord
from Apps.Parkings.utils.detect_read_plate import detect_license_plate, read_license_plate
import os


# =========================================================
# CHECK-IN
# =========================================================
def handle_check_in(card_id, vehicle_type, image):
    card = Card.objects.get(id=card_id)

    # --- Tạo thư mục tạm ---
    temp_dir = os.path.join(settings.MEDIA_ROOT, "temp")
    os.makedirs(temp_dir, exist_ok=True)

    # --- Lưu ảnh ---
    image_name = f"{timezone.now().strftime('%Y%m%d%H%M%S')}_{card_id}.jpg"
    image_path = os.path.join(temp_dir, image_name)
    with open(image_path, 'wb+') as dest:
        for chunk in image.chunks():
            dest.write(chunk)

    # --- Gọi AI ---
    crop_path = detect_license_plate(image_path)
    plate_number = read_license_plate(crop_path) if crop_path else "UNKNOWN"

    # --- Ghi record ---
    ParkingRecord.objects.create(
        card=card,
        plate_number=plate_number,
        vehicle_type=vehicle_type,
        image_path=f"temp/{image_name}",
        check_in_time=timezone.now(),
    )

    # --- Cập nhật thẻ ---
    card.status = 'active'
    card.save()

    return plate_number


# =========================================================
# CHECK-OUT THÀNH CÔNG
# =========================================================
def check_out_successful(record, card):
    record.check_out_time = timezone.now()

    # Xóa ảnh check-in nếu còn
    if record.image_path:
        full_path = os.path.join(settings.MEDIA_ROOT, record.image_path)
        if os.path.exists(full_path):
            os.remove(full_path)
        record.image_path = None

    record.save()

    # Đổi trạng thái thẻ
    card.status = 'inactive'
    card.save()

    return {"success": True, "message": "Check-out thành công."}


# =========================================================
# XÁC MINH THỦ CÔNG
# =========================================================
def handle_manual_auth(record_id, confirm, from_lost_card):
    try:
        record = ParkingRecord.objects.get(id=record_id)
        card = record.card
    except ParkingRecord.DoesNotExist:
        return {"error": "Không tìm thấy bản ghi xác minh."}

    if confirm == "yes":
        result = check_out_successful(record, card)
        if from_lost_card:
            card.status = 'disable'
            card.save()
            result["message"] += " (Thẻ đã bị vô hiệu hóa.)"
        return result
    else:
        return {"failed": True, "reason": "Check-out bị hủy bởi quản lý."}


# =========================================================
# CHECK-OUT
# =========================================================
def handle_check_out(card_id, uploaded_image):
    try:
        card = Card.objects.get(id=card_id)
    except Card.DoesNotExist:
        return {"error": "Không tìm thấy thẻ này."}

    record = ParkingRecord.objects.filter(card=card, check_out_time__isnull=True).last()
    if not record:
        return {"error": "Không tìm thấy lượt đỗ đang hoạt động cho thẻ này."}

    # --- Tạo file tạm ---
    temp_dir = os.path.join(settings.MEDIA_ROOT, "temp")
    os.makedirs(temp_dir, exist_ok=True)
    temp_name = f"{timezone.now().strftime('%Y%m%d%H%M%S')}_{card_id}.jpg"
    temp_path = os.path.join(temp_dir, temp_name)

    with open(temp_path, 'wb+') as f:
        for chunk in uploaded_image.chunks():
            f.write(chunk)

    # --- Gọi AI ---
    crop_path = detect_license_plate(temp_path)
    plate_number = read_license_plate(crop_path) if crop_path else "UNKNOWN"

    # Xóa ảnh tạm
    if os.path.exists(temp_path):
        os.remove(temp_path)

    # --- So khớp ---
    if plate_number.lower() != record.plate_number.lower():
        return {
            "mismatch": True,
            "check_in_image_path": f"{settings.MEDIA_URL}{record.image_path}" if record.image_path else None,
            "record_id": record.id,
            "ai_plate": plate_number,
            "db_plate": record.plate_number,
        }

    # --- Nếu khớp ---
    return check_out_successful(record, card)


# =========================================================
# MẤT THẺ
# =========================================================
def handle_lost_card(card_id):
    try:
        card = Card.objects.get(id=card_id)
    except Card.DoesNotExist:
        return {"error": "Thẻ không tồn tại hoặc đã bị vô hiệu hóa."}

    if card.status == 'inactive':
        card.status = 'disable'
        card.save()
        return {"success": True, "message": f"Thẻ {card.id} đã bị vô hiệu hóa."}

    elif card.status == 'active':
        record = ParkingRecord.objects.filter(card=card, check_out_time__isnull=True).first()
        if not record:
            return {"error": "Không tìm thấy lượt gửi xe hợp lệ."}

        return {
            "need_verification": True,
            "record_id": record.id
        }

    else:
        return {"warning": f"Thẻ {card.id} đã bị vô hiệu hóa hoặc không hợp lệ."}