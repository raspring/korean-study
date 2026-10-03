from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: str
    name: Optional[str]

    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


class CardProgressUpdate(BaseModel):
    category: str
    card_kr: str
    known: bool


class CardProgressOut(BaseModel):
    category: str
    card_kr: str
    known: bool

    model_config = {"from_attributes": True}


class QuizScoreCreate(BaseModel):
    category: str
    score: int
    total: int
    direction: str


class QuizScoreOut(BaseModel):
    id: int
    category: str
    score: int
    total: int
    direction: str
    created_at: datetime

    model_config = {"from_attributes": True}
