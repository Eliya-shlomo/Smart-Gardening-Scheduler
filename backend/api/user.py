from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError
from sqlalchemy.orm import Session
from fastapi import Body
from backend.schemas.user import UserCreate, UserLogin, UserResponse, Token
from backend.database import get_db
from backend.crud.user import get_user_by_email,create_user, authenticate_user
from backend.utils.security import create_access_token
from backend.api.deps import get_current_user
from backend.utils.security import create_access_token, create_refresh_token_string
from backend.crud.refresh_token import create_refresh_token, get_valid_refresh_token,revoke_refresh_token
from backend import models
from backend.crud.audit_log import create_log


router = APIRouter(prefix="/users", tags=["Users"])

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

### All three function down - depends on frontend implementation
# to use the token on cookie or other benefits of token saved on db 
@router.post("/login", response_model=Token)
def login(login_data: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, login_data.email, login_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token_str = create_refresh_token_string()
    create_refresh_token(db, refresh_token_str, user.id)

    # Audit Log for login
    create_log(
        db=db,
        user_id=user.id,
        action="login",
        entity_type="User",
        details=f"User {user.email} logged in"
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token_str,
        "token_type": "bearer"
    }


@router.post("/refresh-token", response_model=Token)
def refresh_token(
    refresh_token: str = Body(...),
    db: Session = Depends(get_db)
):

    token_record = get_valid_refresh_token(db, refresh_token)
    if not token_record:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    access_token = create_access_token(data={"sub": str(token_record.user_id)})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.get("/me", response_model=UserResponse)
def read_current_user(current_user: UserResponse = Depends(get_current_user)):
    return current_user


@router.post("/logout")
def logout(
    refresh_token: str = Body(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    token_record = get_valid_refresh_token(db, refresh_token)
    if not token_record or token_record.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized token")

    revoke_refresh_token(db, refresh_token)

    # Audit Log for logout
    create_log(
        db=db,
        user_id=current_user.id,
        action="logout",
        entity_type="User",
        details=f"User {current_user.email} logged out"
    )

    return {"detail": "Logged out successfully"}
