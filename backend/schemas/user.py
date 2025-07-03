from typing_extensions import Annotated
from pydantic import BaseModel, EmailStr , StringConstraints
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    name: Annotated[str,StringConstraints(pattern=r'^[a-zA-Z0-9_]{3,20}$')] 
    hone: Optional[Annotated[str, StringConstraints(min_length=9,max_length=10,pattern=r'^\d+$')]] = None

class UserCreate(UserBase):
    password: Annotated[str,StringConstraints(pattern=r'^[a-zA-Z0-9_]{3,20}$')]

class UserLogin(BaseModel):
    email: EmailStr
    password: Annotated[str,StringConstraints(pattern=r'^[a-zA-Z0-9_]{3,20}$')]

class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: Optional[int] = None
