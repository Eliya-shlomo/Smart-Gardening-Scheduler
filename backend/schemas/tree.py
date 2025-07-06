# Tree schema for getting notes for each tree -> lets say the particular tree need's note for his condition or healthy ect
from datetime import datetime
from typing_extensions import Annotated
from pydantic import BaseModel, EmailStr , StringConstraints
from typing import Optional

class TreeBase(BaseModel):
    type: Annotated[str,StringConstraints(pattern=r'^[a-zA-Z_]{3,20}$')] 
    planting_date: Optional[datetime] = None
    notes: Optional[str] = None

class TreeCreate(TreeBase):
    client_id: int  

class TreeUpdate(TreeBase):
    pass

class TreeResponse(TreeBase):
    id: int
    client_id: int

    class Config:
        orm_mode = True
