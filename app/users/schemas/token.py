from pydantic import BaseModel
from users.models.refresh_token import RefreshToken

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
