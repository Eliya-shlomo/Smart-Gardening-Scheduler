from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError
from sqlalchemy.orm import Session
from fastapi import Body
from app.users.schemas.user import UserCreate, UserLogin, UserResponse, Token
from app.users.database import get_db
from app.users.crud import get_user_by_email,create_user, authenticate_user
from app.utils.security import create_access_token
from app.users.api.deps import get_current_user
from app.utils.security import create_access_token, create_refresh_token_string
from app.crud.refresh_token import create_refresh_token, get_valid_refresh_token,revoke_refresh_token
from app.users.models import user
from app.crud.audit_log import create_log


router = APIRouter()


@router.get("/me", response_model=UserResponse)
def read_current_user(current_user: UserResponse = Depends(get_current_user)):
    return current_user