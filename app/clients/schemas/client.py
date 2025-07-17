from typing_extensions import Annotated
from pydantic import BaseModel, EmailStr , StringConstraints
from typing import Optional

hebrew_and_english_pattern = r'^[\u0590-\u05FFa-zA-Z0-9 _-]{3,100}$'

## Annotated option is given to restrict the way data is enter db
class ClientBase(BaseModel):
    name: Annotated[str,StringConstraints(pattern=hebrew_and_english_pattern)]
    email: EmailStr
    address: Annotated[str,StringConstraints(pattern=hebrew_and_english_pattern)]
    phone: Optional[Annotated[str, StringConstraints(min_length=9,max_length=10,pattern=r'^\d+$')]] = None

class ClientCreate(ClientBase):
    pass

class ClientUpdate(ClientBase):
    pass

class ClientResponse(ClientBase):
    id: int
    user_id: int          

    class Config:
        orm_mode = True
