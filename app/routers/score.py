from typing import Annotated, List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from .. import schemas, models, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/scores",  # New prefix for all score-related routes
    tags=["Scores & Leaderboard"]
)

DBSession = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[models.User_model, Depends(oauth2.get_current_user)]

# --- Schema for updating score ---
class ScoreUpdate(BaseModel):
    score: int

@router.get("/me", response_model=schemas.User)
def get_user_me(db: DBSession, current_user: CurrentUser):
    """
    Get the details of the currently authenticated user, including their battle score.
    """
    # Eagerly load the battle_score relationship
    user = db.query(models.User_model).filter(models.User_model.id == current_user.id).one()
    
    # If the user has no score entry yet, create one.
    if not user.battle_score:
        new_score = models.BattleScore(score=0, user_id=user.id)
        db.add(new_score)
        db.commit()
        db.refresh(user)

    return user

@router.post("/", response_model=schemas.BattleScore)
def update_user_score(score_update: ScoreUpdate, db: DBSession, current_user: CurrentUser):
    """
    Update the user's high score if the new score is higher.
    Creates a score record if one doesn't exist.
    """
    score_record = db.query(models.BattleScore).filter(models.BattleScore.user_id == current_user.id).first()

    if not score_record:
        score_record = models.BattleScore(user_id=current_user.id, score=score_update.score)
    else:
        if score_update.score > score_record.score:
            score_record.score = score_update.score
    
    db.add(score_record)
    db.commit()
    db.refresh(score_record)
    return score_record


@router.get("/leaderboard", response_model=List[schemas.LeaderboardUser])
def get_leaderboard(db: DBSession):
    """
    Get the top 10 players by joining User and BattleScore tables.
    """
    top_scores = (
        db.query(
            models.User_model.username,
            models.BattleScore.score.label("high_score")
        )
        .join(models.BattleScore, models.User_model.id == models.BattleScore.user_id)
        .order_by(models.BattleScore.score.desc())
        .limit(10)
        .all()
    )
    return top_scores
