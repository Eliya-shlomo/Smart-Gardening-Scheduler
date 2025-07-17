# Tree schema for getting notes for each tree -> lets say the particular tree need's note for his condition or healthy ect
from datetime import datetime
from typing_extensions import Annotated
from pydantic import BaseModel, StringConstraints
from typing import Optional

hebrew_and_english_pattern = r'^[\u0590-\u05FFa-zA-Z0-9 _-]{3,100}$'

## Annotated option is given to restrict the way data is enter db
class TreeBase(BaseModel):
    type: Annotated[str,StringConstraints(pattern=hebrew_and_english_pattern)] 
    planting_date: Optional[datetime] = None
    notes: Optional[Annotated[str,StringConstraints(pattern=hebrew_and_english_pattern)] ] = None

class TreeCreate(TreeBase):
    client_id: int  

class TreeUpdate(TreeBase):
    pass

class TreeResponse(TreeBase):
    id: int
    client_id: int

    class Config:
        orm_mode = True
