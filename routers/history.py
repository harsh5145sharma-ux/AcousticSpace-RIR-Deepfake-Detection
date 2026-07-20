"""
History routes — user apne past predictions dekh sakta hai.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
import models
import schemas
from auth import get_current_user

router = APIRouter(prefix="/history", tags=["History"])


@router.get("/", response_model=List[schemas.PredictionOut])
def get_history(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Logged-in user ki saari past predictions return karta hai."""
    predictions = (
        db.query(models.Prediction)
        .filter(models.Prediction.owner_id == current_user.id)
        .order_by(models.Prediction.created_at.desc())
        .all()
    )
    return predictions


@router.get("/{prediction_id}", response_model=schemas.PredictionOut)
def get_prediction_by_id(
    prediction_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Ek specific prediction detail se dekhne ke liye — sirf apni hi dekh sakte ho."""
    prediction = (
        db.query(models.Prediction)
        .filter(
            models.Prediction.id == prediction_id,
            models.Prediction.owner_id == current_user.id,
        )
        .first()
    )
    if not prediction:
        raise HTTPException(status_code=404, detail="Prediction not found")
    return prediction
