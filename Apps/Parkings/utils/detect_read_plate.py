import requests
import cv2
import os
import easyocr
import numpy as np
import re

ROBOFLOW_API_URL = "https://detect.roboflow.com/license-plate-recognition-obuwl/2"
API_KEY = "IVELRMTdw2CrLqYsBkvp"

def detect_license_plate(image_path, output_dir="output"):
    """Phát hiện vùng chứa biển số và lưu ảnh crop ra file."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    response = requests.post(
        f"{ROBOFLOW_API_URL}?api_key={API_KEY}",
        files={"file": open(image_path, "rb")}
    )
    result = response.json()

    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Không tìm thấy ảnh: {image_path}")

    predictions = result.get("predictions", [])
    if not predictions:
        return None

    best_pred = max(predictions, key=lambda x: x["confidence"])
    x, y, w, h = int(best_pred["x"]), int(best_pred["y"]), int(best_pred["width"]), int(best_pred["height"])
    x1, y1 = max(x - w // 2, 0), max(y - h // 2, 0)
    x2, y2 = x + w // 2, y + h // 2

    plate_crop = image[y1:y2, x1:x2]
    crop_path = os.path.join(output_dir, "plate_crop.jpg")
    cv2.imwrite(crop_path, plate_crop)
    return crop_path


def read_license_plate(plate_image_path):
    """Đọc ký tự từ ảnh biển số (EasyOCR + xử lý ký tự)."""
    if not os.path.exists(plate_image_path):
        raise FileNotFoundError(f"Không tìm thấy ảnh: {plate_image_path}")

    reader = easyocr.Reader(['en', 'vi'], gpu=False)
    image = cv2.imread(plate_image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    gray = cv2.convertScaleAbs(gray, alpha=1.6, beta=10)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    gray = cv2.filter2D(gray, -1, kernel)
    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
    gray = clahe.apply(gray)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    cv2.imwrite("output/plate_preprocessed.jpg", thresh)

    results = reader.readtext(thresh, detail=0, allowlist='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    if not results:
        return ""

    text = ''.join(results).replace(" ", "")
    confusion_map = {'0': 'O', 'O': '0', '1': 'I', 'I': '1', '2': 'Z', 'Z': '2',
                     'L': '4', '4': 'L', '5': 'S', 'S': '5', '8': 'B', 'B': '8'}

    if len(text) > 9:
        text = text[:9]
    elif len(text) < 7:
        return text

    def is_letter(ch): return ch.isalpha()
    if not is_letter(text[2]):
        if text[2] in confusion_map:
            text = text[:2] + confusion_map[text[2]].upper() + text[3:]
            text = ''.join(
                confusion_map[c] if c in confusion_map and confusion_map[c].isdigit() else c
                for c in text
            )

    pattern = r"\d{2}[A-Z]{1,2}\d{4,6}"
    match = re.search(pattern, text)
    if match:
        text = match.group()

    return text