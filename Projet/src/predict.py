import os, json
import numpy as np
from tensorflow import keras
from src.preprocess import preprocess_image

_BASE = os.path.join(os.path.dirname(__file__), "..", "data")
_model = keras.models.load_model(os.path.join(_BASE, "cnn_final.keras"))
with open(os.path.join(_BASE, "idx_to_letter.json")) as f:
    _idx_to_letter = {int(k): v for k, v in json.load(f).items()}

THRESHOLD = 0.7


def predict(img_bgr):
    """Image BGR -> (lettre, confiance, fiable)."""
    x = preprocess_image(img_bgr)[None, ...]
    proba = _model.predict(x, verbose=0)[0]
    idx = int(proba.argmax())
    conf = float(proba[idx])
    return _idx_to_letter[idx], conf, conf >= THRESHOLD