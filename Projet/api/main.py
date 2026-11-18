import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import cv2
import numpy as np
from fastapi import FastAPI, File, UploadFile, HTTPException
from src.predict import predict

app = FastAPI(title="Sign Letter API")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
async def predict_letter(file: UploadFile = File(...)):
    data = await file.read()
    img = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
    if img is None:
        raise HTTPException(status_code=400, detail="Image illisible")
    letter, conf, reliable = predict(img)
    return {"letter": letter, "confidence": round(conf, 4), "reliable": reliable}