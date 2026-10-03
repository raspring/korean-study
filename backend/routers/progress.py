from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from dependencies import get_current_user
from models import User, CardProgress
from schemas import CardProgressUpdate, CardProgressOut

router = APIRouter()


@router.get("", response_model=List[CardProgressOut])
def get_progress(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return current_user.progress


@router.put("")
def update_progress(
    data: CardProgressUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    row = (
        db.query(CardProgress)
        .filter_by(user_id=current_user.id, category=data.category, card_kr=data.card_kr)
        .first()
    )
    if row:
        row.known = data.known
    else:
        row = CardProgress(user_id=current_user.id, **data.model_dump())
        db.add(row)
    db.commit()
    return {"ok": True}
