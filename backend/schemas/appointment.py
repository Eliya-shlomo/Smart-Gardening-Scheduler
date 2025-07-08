from enum import Enum
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, StringConstraints
from typing_extensions import Annotated

hebrew_and_english_pattern = r'^[\u0590-\u05FFa-zA-Z0-9 _-]{3,100}$'

## Annotated option is given to restrict the way data is enter db
class AppointmentStatus(str, Enum):
    scheduled = "scheduled"
    done = "done"

class AppointmentBase(BaseModel):
    date: datetime
    time: Annotated[str,StringConstraints(pattern=r'^\d{2}:\d{2}$')] = None 
    treatment_type: Annotated[str,StringConstraints(pattern=hebrew_and_english_pattern)]
    notes: Optional[Annotated[str,StringConstraints(pattern=hebrew_and_english_pattern)]] = None

class AppointmentCreate(AppointmentBase):
    client_id: int

class AppointmentUpdate(BaseModel):
    status: AppointmentStatus
    notes: Optional[Annotated[str,StringConstraints(pattern=hebrew_and_english_pattern)]] = None

class AppointmentResponse(AppointmentBase):
    id: int
    client_id: int
    status: AppointmentStatus

    class Config:
        orm_mode = True
