from django.shortcuts import render, redirect
from django.contrib import messages
from BTL_Python import settings
from .models import Card, ParkingRecord
from . import services


# ==============================
# Trang chính
# ==============================
def index(request):
    return render(request, "parkings/base.html")


# ==============================
# Check-in
# ==============================
def check_in(request):
    inactive_cards = Card.objects.filter(status='inactive')
    if request.method == 'POST':
        card_id = request.POST.get('card_id')
        vehicle_type = request.POST.get('vehicle_type')
        image = request.FILES.get('image')

        if not all([card_id, image, vehicle_type]):
            messages.error(request, "⚠️ Thiếu thông tin check-in.")
        else:
            plate = services.handle_check_in(card_id, vehicle_type, image)
            messages.success(request, f"✅ Check-in thành công! Biển số: {plate}")

    return render(request, "parkings/check_in.html", {"cards": inactive_cards})


# ==============================
# Check-out
# ==============================
def check_out(request):
    active_cards = Card.objects.filter(status='active')
    context = {"cards": active_cards, "mismatch_record": None}

    if request.method == 'POST':
        card_id = request.POST.get('card_id')
        image = request.FILES.get('image')

        if not all([card_id, image]):
            messages.error(request, "⚠️ Vui lòng chọn thẻ và tải ảnh check-out.")
        else:
            result = services.handle_check_out(card_id, image)

            if result.get("mismatch"):
                context["mismatch_record"] = result
                messages.warning(request, "⚠️ Biển số không khớp, cần xác minh thủ công.")
            elif result.get("success"):
                messages.success(request, result["message"])
                return redirect("Parkings:check_out")
            elif result.get("error"):
                messages.error(request, result["error"])

    return render(request, "parkings/check_out.html", context)


# ==============================
# Manual Authentication
# ==============================
def manual_authentication(request, record_id):
    if request.method == "POST":
        confirm = request.POST.get("confirm")
        from_lost_card = request.POST.get("from_lost_card") == "true"

        result = services.handle_manual_auth(record_id, confirm, from_lost_card)

        if result.get("success"):
            messages.success(request, f"✅ {result['message']}")
        elif result.get("failed"):
            messages.warning(request, result["reason"])
        else:
            messages.error(request, result.get("error", "Lỗi xác minh."))

    return redirect("Parkings:check_out")


# ==============================
# Lost Card
# ==============================
def lost_card(request):
    if request.method == "POST":
        card_id = request.POST.get("card_id")
        if not card_id:
            messages.error(request, "⚠️ Vui lòng nhập mã thẻ.")
            return redirect("Parkings:check_out")

        result = services.handle_lost_card(card_id)

        if result.get("need_verification"):
            record = ParkingRecord.objects.get(id=result["record_id"])
            return render(request, "Parkings/check_out.html", {
                "lost_mode": True,
                "record": record,
                "from_lost_card": "true",
                "check_in_image_url": settings.MEDIA_URL + record.image_path if record.image_path else None,
            })
        elif result.get("success"):
            messages.success(request, result["message"])
        elif result.get("warning"):
            messages.warning(request, result["warning"])
        elif result.get("error"):
            messages.error(request, result["error"])

    return redirect("Parkings:check_out")


# ==============================
# Parking history
# ==============================
def parking_history(request):
    def normalize(value):
        if value in [None, '', 'None']:
            return ''
        return value.strip()

    plate = normalize(request.GET.get('plate'))
    card_id = normalize(request.GET.get('card_id'))
    vehicle_type = normalize(request.GET.get('vehicle_type'))
    status = normalize(request.GET.get('status'))
    start_date = normalize(request.GET.get('start_date'))
    end_date = normalize(request.GET.get('end_date'))

    records = ParkingRecord.objects.all().order_by('-check_in_time')

    if plate:
        records = records.filter(plate_number=plate)

    if card_id:
        records = records.filter(card__id=card_id)

    if vehicle_type:
        records = records.filter(vehicle_type=vehicle_type)

    if status == 'checked_in':
        records = records.filter(check_out_time__isnull=True)
    elif status == 'checked_out':
        records = records.filter(check_out_time__isnull=False)

    if start_date:
        records = records.filter(check_in_time__date__gte=start_date)
    if end_date:
        records = records.filter(check_in_time__date__lte=end_date)

    context = {
        "records": records,
        "filters": {
            "plate": plate,
            "card_id": card_id,
            "vehicle_type": vehicle_type,
            "status": status,
            "start_date": start_date,
            "end_date": end_date,
        }
    }

    return render(request, "Parkings/history.html", context)


# ==============================
# Add Card
# ==============================
def add_card(request):
    if request.method == 'POST':
        new_card = Card.objects.create(status='inactive')
        messages.success(request, f"✅ Thêm thẻ thành công! Mã thẻ mới: {new_card.id}")
        return redirect(request.path)

    cards = Card.objects.all().order_by('-id')
    return render(request, 'parkings/add_card.html', {'cards': cards})