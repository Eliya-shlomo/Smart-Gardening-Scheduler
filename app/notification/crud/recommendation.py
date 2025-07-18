from sqlalchemy.orm import Session
from datetime import datetime
from notification.models.recommendation import Recommendation
from notification.schemas.recommendation import RecommendationCreate

def create_recommendation(db: Session, rec_in: RecommendationCreate):
    rec = Recommendation(**rec_in.model_dump())
    db.add(rec)
    db.commit()
    db.refresh(rec)
    return rec

def get_recommendation(db: Session, rec_id: int):
    return db.query(Recommendation).filter(Recommendation.id == rec_id).first()

def get_all_recommendations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Recommendation).offset(skip).limit(limit).all()

def delete_recommendation(db: Session, rec_id: int):
    rec = get_recommendation(db, rec_id)
    if rec:
        db.delete(rec)
        db.commit()
    return rec

def was_recommendation_sent_this_month(db: Session, tree_id: int, type_: str) -> bool:
    now = datetime.now()
    start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    return db.query(Recommendation).filter(
        Recommendation.tree_id == tree_id,
        Recommendation.type == type_,
        Recommendation.send_date >= start_of_month
    ).first() is not None
