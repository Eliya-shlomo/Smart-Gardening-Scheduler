from pydantic import BaseModel, StringConstraints
from datetime import datetime
from typing import Optional
from typing_extensions import Annotated

hebrew_and_english_pattern = r'^[\u0590-\u05FFa-zA-Z0-9 _-]{3,100}$'

class RecommendationBase(BaseModel):
    type: Annotated[str,StringConstraints(pattern=hebrew_and_english_pattern)] 
    notes: Optional[Annotated[str,StringConstraints(pattern=hebrew_and_english_pattern)] ] = None

class RecommendationCreate(RecommendationBase):
    tree_id: int

class RecommendationResponse(RecommendationBase):
    id: int
    tree_id: int
    send_date: datetime

    class Config:
        orm_mode = True
