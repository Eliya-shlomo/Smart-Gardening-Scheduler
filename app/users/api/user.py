from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError
from sqlalchemy.orm import Session
from fastapi import Body
from users.schemas.user import UserCreate, UserLogin, UserResponse, Token
from users.database import get_db
from users.crud.user import get_user_by_email,create_user, authenticate_user
from users.utils.security import create_access_token
from users.utils.deps import get_current_user
from users.utils.security import create_access_token, create_refresh_token_string
from users.crud.refresh_token import create_refresh_token, get_valid_refresh_token,revoke_refresh_token
from users.models.user import User


router = APIRouter()


@router.get("/me", response_model=UserResponse)
def read_current_user(current_user: UserResponse = Depends(get_current_user)):
    return current_user