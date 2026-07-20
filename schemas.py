"""
Pydantic schemas — request validation aur response formatting ke liye.
"""

from pydantic import BaseModel, EmailStr
from datetime import datetime


# ---------- Auth Schemas ----------

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    username: str | None = None


# ---------- Prediction Schemas ----------

class PredictionOut(BaseModel):
    id: int
    filename: str
    result: str
    confidence: float
    created_at: datetime

    class Config:
        from_attributes = True


class PredictionResponse(BaseModel):
    prediction: str
    confidence: float
    filename: str
