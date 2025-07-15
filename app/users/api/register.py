from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError
from sqlalchemy.orm import Session
from fastapi import Body
from app.users.schemas.user import UserCreate, UserLogin, UserResponse, Token
from app.users.database import get_db
from app.users.crud.user import get_user_by_email,create_user, authenticate_user
from app.utils.security import create_access_token
from app.users.api.deps import get_current_user
from app.utils.security import create_access_token, create_refresh_token_string
from app.crud.refresh_token import create_refresh_token, get_valid_refresh_token,revoke_refresh_token
from app.users.models import user
from app.crud.audit_log import create_log


router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    existing_user = get_user_by_email(db, user_in.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    try:
        new_user = create_user(db, user_in)
    except ValidationError as e:
        raise HTTPException(
            status_code=422,
            detail=f"Invalid input: {e.errors()}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Could not create user: {str(e)}"
        )

    return new_user





