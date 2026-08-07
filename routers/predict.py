import os
import shutil
import uuid

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
)

from sqlalchemy.orm import Session

from database import get_db
from auth import get_current_user

import models

from services.ml_service import (
    MLIntegrationError,
    predict_audio_file,
)


router = APIRouter(
    prefix="/predict",
    tags=["Prediction"],
)


UPLOAD_DIR = "uploads"

MAX_FILE_SIZE = 20 * 1024 * 1024

ALLOWED_EXTENSIONS = {
    ".wav",
    ".mp3",
    ".flac",
}


os.makedirs(
    UPLOAD_DIR,
    exist_ok=True,
)


@router.post("/")
def predict_audio(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(
        get_current_user
    ),
):

    # ---------------------------------
    # Validate filename
    # ---------------------------------

    if not file.filename:

        raise HTTPException(
            status_code=400,
            detail="Audio filename is required.",
        )

    extension = os.path.splitext(
        file.filename
    )[1].lower()

    # ---------------------------------
    # Validate extension
    # ---------------------------------

    if extension not in ALLOWED_EXTENSIONS:

        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported audio format. "
                "Allowed formats: WAV, MP3, FLAC."
            ),
        )

    # ---------------------------------
    # Unique temporary filename
    # ---------------------------------

    temporary_name = (
        f"{uuid.uuid4().hex}{extension}"
    )

    file_path = os.path.join(
        UPLOAD_DIR,
        temporary_name,
    )

    try:

        # ---------------------------------
        # Save uploaded audio
        # ---------------------------------

        with open(
            file_path,
            "wb",
        ) as buffer:

            shutil.copyfileobj(
                file.file,
                buffer,
            )

        # ---------------------------------
        # Validate size
        # ---------------------------------

        if os.path.getsize(file_path) > MAX_FILE_SIZE:

            raise HTTPException(
                status_code=413,
                detail="Maximum audio size is 20 MB.",
            )

        # ---------------------------------
        # Member 1 -> Member 2
        # ---------------------------------

        try:

            result = predict_audio_file(
                file_path
            )

        except MLIntegrationError as exc:

            raise HTTPException(
                status_code=503,
                detail=str(exc),
            )

        # ---------------------------------
        # Store history
        # ---------------------------------

        record = models.Prediction(
            filename=file.filename,
            result=result["prediction"],
            confidence=result["confidence"],
            owner_id=current_user.id,
        )

        db.add(record)

        db.commit()

        db.refresh(record)

        # ---------------------------------
        # Response for Member 4
        # ---------------------------------

        return {
            "id": record.id,
            "filename": file.filename,
            "prediction": result["prediction"],
            "confidence": result["confidence"],
            "flagged_segments": result.get(
                "flagged_segments",
                [],
            ),
            "created_at": record.created_at,
        }

    finally:

        try:
            file.file.close()
        except Exception:
            pass

        if os.path.exists(file_path):
            os.remove(file_path)