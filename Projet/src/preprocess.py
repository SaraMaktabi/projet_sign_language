import os
import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision

_MODEL = os.path.join(os.path.dirname(__file__), "..", "data", "hand_landmarker.task")

_landmarker = vision.HandLandmarker.create_from_options(
    vision.HandLandmarkerOptions(
        base_options=mp_python.BaseOptions(model_asset_path=_MODEL),
        num_hands=1,
        min_hand_detection_confidence=0.3,
    )
)
_clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(4, 4))


def crop_hand(img_bgr, margin=0.25):
    """Recadre autour de la main. Retourne None si aucune main détectée."""
    rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    mp_img = mp.Image(image_format=mp.ImageFormat.SRGB, data=np.ascontiguousarray(rgb))
    res = _landmarker.detect(mp_img)
    if not res.hand_landmarks:
        return None
    h, w = img_bgr.shape[:2]
    pts = np.array([[l.x * w, l.y * h] for l in res.hand_landmarks[0]])
    x0, y0 = pts.min(0)
    x1, y1 = pts.max(0)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    s = max(x1 - x0, y1 - y0) * (1 + 2 * margin)
    x0, x1 = int(max(cx - s / 2, 0)), int(min(cx + s / 2, w))
    y0, y1 = int(max(cy - s / 2, 0)), int(min(cy + s / 2, h))
    return img_bgr[y0:y1, x0:x1]


def preprocess_image(img_bgr):
    """Image BGR quelconque -> (28, 28, 1) float32 dans [0, 1]."""
    crop = crop_hand(img_bgr)
    if crop is None or crop.size == 0:
        crop = img_bgr  # repli : image entière
    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape
    s = min(h, w)
    y0, x0 = (h - s) // 2, (w - s) // 2
    gray = gray[y0:y0 + s, x0:x0 + s]
    small = cv2.resize(gray, (28, 28), interpolation=cv2.INTER_AREA)
    # small = _clahe.apply(small)
    
    return (small.astype("float32") / 255.0).reshape(28, 28, 1)