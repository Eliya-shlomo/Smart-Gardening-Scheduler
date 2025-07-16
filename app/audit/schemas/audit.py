from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AuditLogResponse(BaseModel):
    id: int
    user_id: int   
    action: str
    entity_type: str
    entity_id: Optional[int]
    details: Optional[str]
    timestamp: datetime

    class Config:
        from_attributes = True  



class AuditLogCreate(BaseModel):
    user_id: int
    action: str
    entity_type: str
    entity_id: Optional[int] = None
    details: Optional[str] = None
