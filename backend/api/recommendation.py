from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.schemas.recommendation import RecommendationResponse
from backend.api.deps import get_current_user
from backend import models

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])

@router.get("/my", response_model=list[RecommendationResponse])
def get_my_recommendations(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    recommendations = db.query(models.Recommendation).join(models.Tree).join(models.Client).filter(
        models.Client.user_id == current_user.id
    ).all()
    return recommendations
