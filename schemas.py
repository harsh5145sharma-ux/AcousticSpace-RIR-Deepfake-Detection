"""
Pydantic schemas — request validation aur response formatting ke liye.
"""

from pydantic import BaseModel, EmailStr
from datetime import datetime


# ---------- Auth Schemas ----------

from pydantic import BaseModel, EmailStr, Field
"""
Schema used during user registration.
"""
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=30)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=64)

"""
Schema returned after successful registration.
"""
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

"""
Prediction response returned to authenticated users.
"""
class PredictionResponse(BaseModel):
    prediction: str
    confidence: float
    filename: str
