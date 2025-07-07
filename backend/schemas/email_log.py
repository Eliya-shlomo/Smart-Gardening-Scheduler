from pydantic import BaseModel, EmailStr, StringConstraints
from datetime import datetime
from typing_extensions import Annotated

hebrew_and_english_pattern = r'^[\u0590-\u05FFa-zA-Z0-9 _-]{3,100}$'

class EmailLogResponse(BaseModel):
    id: int
    template_name: Annotated[str,StringConstraints(pattern=hebrew_and_english_pattern)] 
    sent_at: datetime
    recipient_email: EmailStr
    status: Annotated[str,StringConstraints(pattern=hebrew_and_english_pattern)] 

    class Config:
        orm_mode = True
