from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.users.schemas.user import UserLogin
from app.users.schemas.token import Token
from app.users.crud.user import authenticate_user
from app.utils.security import create_access_token, create_refresh_token_string
from app.users.crud.refresh_token import create_refresh_token
from app.users.database import get_db
from app.crud.audit_log import create_log

router = APIRouter()


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



