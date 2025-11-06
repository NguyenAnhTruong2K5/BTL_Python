from Apps.Parkings.utils.detect_read_plate import detect_license_plate, read_license_plate

def solve_plate(image_path):
    """Pipeline phát hiện & đọc biển số"""
    crop_path = detect_license_plate(image_path)
    if not crop_path:
        print("❌ Không phát hiện được biển số trong ảnh.")
        return None

    plate_number = read_license_plate(crop_path)
    return plate_number