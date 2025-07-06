from enum import Enum
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, StringConstraints
from typing_extensions import Annotated


class AppointmentStatus(str, Enum):
    scheduled = "scheduled"
    done = "done"

class AppointmentBase(BaseModel):
    date: datetime
    time: Annotated[str,StringConstraints(pattern=r'^[0-9_-]{3,50}$')] = None 
    treatment_type: Annotated[str,StringConstraints(pattern=r'^[a-zA-Z0-9_]{3,50}$')]
    notes: Optional[Annotated[str,StringConstraints(pattern=r'^[a-zA-Z0-9_]{3,100}$')]] = None

class AppointmentCreate(AppointmentBase):
    client_id: int

class AppointmentUpdate(BaseModel):
    status: AppointmentStatus
    notes: Optional[Annotated[str,StringConstraints(pattern=r'^[a-zA-Z0-9_]{3,100}$')]] = None

class AppointmentResponse(AppointmentBase):
    id: int
    client_id: int
    status: AppointmentStatus

    class Config:
        orm_mode = True
