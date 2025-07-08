from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AuditLogResponse(BaseModel):
    id: int
    action: str
    entity_type: str
    entity_id: Optional[int]
    details: Optional[str]
    timestamp: datetime

    class Config:
        orm_mode = True
