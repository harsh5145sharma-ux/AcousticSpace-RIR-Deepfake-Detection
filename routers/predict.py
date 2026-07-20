"""
Prediction route — audio file leke real/fake prediction deta hai.

IMPORTANT: Abhi 'mock_predict()' use ho raha hai kyunki Member 2 ka
trained model (model.pt) abhi ready nahi hai. Jaise hi model mil jaye,
neeche diye MOCK ko REAL FUNCTION se replace karna hai — instructions
niche comment mein hain.
"""

import random
import shutil
import os
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session

from database import get_db
import models
import schemas
from auth import get_current_user

router = APIRouter(prefix="/predict", tags=["Prediction"])

ALLOWED_EXTENSIONS = {".wav", ".flac", ".mp3"}
MAX_FILE_SIZE_MB = 20
UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


# ============================================================
# MOCK PREDICTION — TEMPORARY, Member 2 ka model aane tak
# ============================================================
def mock_predict(file_path: str) -> dict:
    """
    Dummy prediction function. Real/fake randomly return karta hai
    taaki API ka structure test ho sake bina real model ke.

    Member 2 ka model.pt ready hone par isko is se replace karo:

    import torch
    from preprocessing import extract_features  # Member 1 ka pipeline

    def real_predict(file_path: str) -> dict:
        model = torch.load("model.pt")
        model.eval()
        features = extract_features(file_path)
        with torch.no_grad():
            output = model(features)
        prediction = "fake" if output.item() > 0.5 else "real"
        confidence = float(output.item())
        return {"prediction": prediction, "confidence": confidence}
    """
    prediction = random.choice(["real", "fake"])
    confidence = round(random.uniform(0.70, 0.99), 2)
    return {"prediction": prediction, "confidence": confidence}


# ============================================================


def validate_file(file: UploadFile):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{ext}'. Allowed: {ALLOWED_EXTENSIONS}",
        )


@router.post("/", response_model=schemas.PredictionResponse)
def predict_audio(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    validate_file(file)

    # File temporarily save karo
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
    if file_size_mb > MAX_FILE_SIZE_MB:
        os.remove(file_path)
        raise HTTPException(
            status_code=400,
            detail=f"File too large ({file_size_mb:.1f}MB). Max allowed: {MAX_FILE_SIZE_MB}MB",
        )

    # ---- Yahan mock_predict() ko real_predict() se replace karna hoga ----
    result = mock_predict(file_path)

    # DB mein prediction save karo (history ke liye)
    db_prediction = models.Prediction(
        filename=file.filename,
        result=result["prediction"],
        confidence=result["confidence"],
        owner_id=current_user.id,
    )
    db.add(db_prediction)
    db.commit()
    db.refresh(db_prediction)

    # Temp file cleanup
    os.remove(file_path)

    return schemas.PredictionResponse(
        prediction=result["prediction"],
        confidence=result["confidence"],
        filename=file.filename,
    )
