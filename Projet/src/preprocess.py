import cv2
import numpy as np


def preprocess_image(img_bgr: np.ndarray) -> np.ndarray:
    """Image BGR quelconque -> tableau (28, 28, 1) float32 dans [0, 1]."""
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

    # Recadrage carré centré
    h, w = gray.shape
    s = min(h, w)
    y0, x0 = (h - s) // 2, (w - s) // 2
    gray = gray[y0:y0 + s, x0:x0 + s]

    # Redimensionnement en 28x28
    small = cv2.resize(gray, (28, 28), interpolation=cv2.INTER_AREA)
    return (small.astype("float32") / 255.0).reshape(28, 28, 1)