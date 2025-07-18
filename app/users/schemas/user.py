from typing_extensions import Annotated
from pydantic import BaseModel, EmailStr , StringConstraints
from typing import Optional

hebrew_and_english_pattern = r'^[\u0590-\u05FFa-zA-Z0-9 _\-!@#$%^&*()+=.]{3,100}$'

## Annotated option is given to restrict the way data is enter db
class UserBase(BaseModel):
    email: EmailStr
    name: Annotated[str,StringConstraints(pattern=hebrew_and_english_pattern)] 
    phone: Annotated[str, StringConstraints(min_length=9,max_length=10,pattern=r'^\d+$')]

class UserCreate(UserBase):
    password: Annotated[str,StringConstraints(pattern=hebrew_and_english_pattern)]

class UserLogin(BaseModel):
    email: EmailStr
    password: Annotated[str,StringConstraints(pattern=hebrew_and_english_pattern)]

class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: Optional[int] = None
