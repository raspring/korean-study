from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from dependencies import get_current_user
from models import User, QuizScore
from schemas import QuizScoreCreate, QuizScoreOut

router = APIRouter()


@router.get("/scores", response_model=List[QuizScoreOut])
def get_scores(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return (
        db.query(QuizScore)
        .filter_by(user_id=current_user.id)
        .order_by(QuizScore.created_at.desc())
        .limit(50)
        .all()
    )


@router.post("/scores", response_model=QuizScoreOut)
def save_score(
    data: QuizScoreCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    score = QuizScore(user_id=current_user.id, **data.model_dump())
    db.add(score)
    db.commit()
    db.refresh(score)
    return score
