from typing_extensions import Annotated
from pydantic import BaseModel, EmailStr , StringConstraints
from typing import Optional

class ClientBase(BaseModel):
    name: Annotated[str,StringConstraints(pattern=r'^[a-zA-Z0-9_]{3,20}$')]
    email: EmailStr
    address: Annotated[str,StringConstraints(pattern=r'^[a-zA-Z0-9_]{3,50}$')]
    phone: Optional[Annotated[str, StringConstraints(min_length=9,max_length=10,pattern=r'^\d+$')]] = None

class ClientCreate(ClientBase):
    pass

class ClientUpdate(ClientBase):
    pass

class ClientResponse(ClientBase):
    id: int

    class Config:
        orm_mode = True
