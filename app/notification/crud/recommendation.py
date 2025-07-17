from sqlalchemy.orm import Session
from datetime import datetime
from backend import models
from backend.schemas.recommendation import RecommendationCreate

def create_recommendation(db: Session, rec_in: RecommendationCreate):
    rec = models.Recommendation(**rec_in.model_dump())
    db.add(rec)
    db.commit()
    db.refresh(rec)
    return rec

def was_recommendation_sent_this_month(db: Session, tree_id: int, type_: str) -> bool:
    now = datetime.now()
    return db.query(models.Recommendation).filter(
        models.Recommendation.tree_id == tree_id,
        models.Recommendation.type == type_,
        models.Recommendation.send_date >= now.replace(day=1, hour=0, minute=0, second=0)
    ).first() is not None
