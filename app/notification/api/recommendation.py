from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from notification.database import get_db
from notification.schemas.recommendation import RecommendationCreate, RecommendationResponse
from notification.crud.recommendation import  was_recommendation_sent_this_month,delete_recommendation as delete_rec,get_all_recommendations,get_recommendation,create_recommendation as create_rec
from notification.utils.dependencies import get_current_user

router = APIRouter(prefix="/recommendation", tags=["recommendation"])

@router.post("/", response_model=RecommendationResponse)
def create_recommendation(
    rec_in: RecommendationCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if was_recommendation_sent_this_month(db, rec_in.tree_id, rec_in.type):
        raise HTTPException(status_code=400, detail="Recommendation already sent this month.")
    return create_rec(db, rec_in)

@router.get("/", response_model=list[RecommendationResponse])
def read_all(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return get_all_recommendations(db, skip, limit)

@router.get("/{rec_id}", response_model=RecommendationResponse)
def read_recommendation(
    rec_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    rec = get_recommendation(db, rec_id)
    if not rec:
        raise HTTPException(status_code=404, detail="Recommendation not found")
    return rec

@router.delete("/{rec_id}", response_model=RecommendationResponse)
def delete_recommendation(
    rec_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    rec = delete_rec(db, rec_id)
    if not rec:
        raise HTTPException(status_code=404, detail="Recommendation not found")
    return rec
